# Create your tasks here
from __future__ import absolute_import, unicode_literals

import uuid

import datetime
from django.contrib.auth.models import User

from account.constants import FORGOT_PASSWORD_OTP_FORMAT, OTP_INFO_KEYS, POSTGRES_JSON_DATETIME_FORMAT
from account.models import Profile
from random import randint
from account.sms_helper import WayToSMSHelper
from waterlily.settings import celery_app, WTS_HELPER
import logging

logger = logging.getLogger('main')


@celery_app.task
def send_sms(mobile, message):
    WTS_HELPER.send_sms(mobile, message)


@celery_app.task
def send_otp_forgot_password(mobile):
    otp = randint(1000, 9999)
    profile = Profile.objects.get(mobile=mobile)
    current_otp_info = {'otp': otp, 'expires_at': (datetime.datetime.now() + datetime.timedelta(minutes=30))
                        .strftime(POSTGRES_JSON_DATETIME_FORMAT), 'otp_used': False}
    otp_info = profile.otp_info
    if otp_info is None:
        otp_info = {OTP_INFO_KEYS['forgot_password']: current_otp_info}
        profile.otp_info = otp_info
    else:
        profile.otp_info[OTP_INFO_KEYS['forgot_password']] = current_otp_info

    profile.save()
    WTS_HELPER.send_sms(mobile, FORGOT_PASSWORD_OTP_FORMAT.format(otp))

# @celery_app.task
# def create_update_user_profile(created, user_id, **kwargs):
#     logger.info('created----->%s %s'%(created, user_id))
#     instance = User.objects.get(id=user_id)
#     if created:
#         Profile.objects.create(user=instance)
#     else:
#         instance.profile = kwargs['validated_data']['profile']
#         instance.save()
#     return
