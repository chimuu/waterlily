import logging

import datetime
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError

from account.constants import OTP_INFO_KEYS, POSTGRES_JSON_DATETIME_FORMAT
from account.models import Profile
from .exceptions import UserAlreadyExists, MobileAlreadyExists, InvalidMobileError, InvalidOTPError

logger = logging.getLogger('main')


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    mobile = serializers.IntegerField()

    @transaction.atomic
    def create(self, validated_data):
        try:
            user = User.objects.create_user(validated_data['username'], '', validated_data['password'])
            # user = User.objects.create_user(validated_data['username'], '', validated_data['password'])
        except IntegrityError as e:
            raise UserAlreadyExists('User already exists')
        else:
            try:
                user.profile.mobile = validated_data["mobile"]
                user.save()
            except IntegrityError as e:
                logger.exception(e)
                raise MobileAlreadyExists('Mobile already exists')
            else:
                return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ForgotUsernamePasswordSerializer(serializers.Serializer):
    mobile = serializers.IntegerField()

    def validate(self, attrs):
        try:
            Profile.objects.get(mobile=attrs['mobile'])
        except Profile.DoesNotExist:
            raise ValidationError('Mobile no does not exist')
        else:
            return attrs


class ResetPasswordSerializer(serializers.Serializer):
    mobile = serializers.IntegerField()
    password = serializers.CharField()
    otp = serializers.IntegerField()

    def validate(self, attrs):
        try:
            self.profile = Profile.objects.get(mobile=attrs['mobile'])
        except Profile.DoesNotExist:
            raise ValidationError('Invalid Mobile no')
        else:
            if self.profile.otp_info[OTP_INFO_KEYS['forgot_password']]['otp'] != attrs['otp']:
                raise ValidationError('Invalid OTP')
            if self.profile.otp_info[OTP_INFO_KEYS['forgot_password']]['otp_used']:
                raise ValidationError('OTP has been used')
            expiry_datetime = self.profile.otp_info[OTP_INFO_KEYS['forgot_password']]['expires_at']
            expiry_datetime = datetime.datetime.strptime(expiry_datetime, POSTGRES_JSON_DATETIME_FORMAT)
            if datetime.datetime.now() > expiry_datetime + datetime.timedelta(minutes=30):
                raise ValidationError('OTP expired')
        return attrs

    def create(self, validated_data):
        self.profile.user.set_password(validated_data['password'])
        self.profile.user.save()
        self.profile.otp_info[OTP_INFO_KEYS['forgot_password']]['otp_used'] = True
        self.profile.save()
        return self.profile.user