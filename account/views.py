from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account import tasks
from account.models import Profile
from .exceptions import UserAlreadyExists, MobileAlreadyExists
from .serializers import LoginSerializer, SignupSerializer, ForgotUsernamePasswordSerializer, ResetPasswordSerializer


class SignupView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except UserAlreadyExists:
            return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except MobileAlreadyExists:
            return Response({"message": "Mobile already exists"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User created successfully"})


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                mobile = Profile.objects.get(user=user).mobile
                return Response({"detail": "User logged in successfully", "username": user.username,
                                 "mobile": mobile})
            else:
                return Response({"detail": "User is no longer active"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Invalid username/password"}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotUsernamePasswordView(APIView):

    def post(self, request):
        serializer = ForgotUsernamePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        tasks.send_otp_forgot_password.delay(serializer.validated_data['mobile'])
        return Response({"message": "OTP sent on registered mobile"})


class ResetPasswordView(APIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        tasks.send_sms.delay(serializer.validated_data['mobile'], 'Password has been successfully reset')
        return Response({"message": "Passsword successfully reset"})


class LogoutView(APIView):

    def get(self, request):
        logout(request)
        return Response({"detail": "Logged out"})


class IsLoggedInView(APIView):

    def get(self, request):
        if request.user.is_authenticated():
            mobile = Profile.objects.get(user=request.user).mobile
            return Response({"detail": "User is logged in", "is_logged_in": True, "username": request.user.username,
                            "mobile": mobile})
        else:
            return Response({"detail": "User is not logged in", "is_logged_in": False}, status=status.HTTP_400_BAD_REQUEST)
