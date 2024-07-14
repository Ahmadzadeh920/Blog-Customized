from django.core import exceptions
from mail_templated import EmailMessage
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import jwt
from ..serializers import (
    RegistrationSerializer,
    CustomeAuthTokenSerializer,
    EmailRequestSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    Customized_TOKEN_OBTAIN_PAIR_SERIALIZER,
    Profile_Serializer,
)

from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from ..permissions import IsVerified

from ....models import CustomUser, PasswordReset, Profile
from ..utils import EmailThread
import os
import time

from_email = "admin@admin.com"


# serializer_class = RegistrationSerializer
class RegisterationApiview(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            obj_user = get_object_or_404(
                CustomUser, email=serializer.validated_data["email"]
            )
            token = self.get_token_for_user(obj_user)
            reset_url = settings.PASSWORD_ACTIVE_BASE_URL + str(token)
            data = {
                "subject": "this email for activation for accounts",
                "message": "plase click this linl for activation of account "
                + "<br/> "
                + str(reset_url),
            }
            Email_obj = EmailMessage(
                "email/activation_accounts.tpl",
                data,
                from_email,
                to=[serializer.validated_data["email"]],
            )
            EmailThread(Email_obj).start()

            return Response(data={"detail": "email send"}, status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={"data": serializer.errors}
        )

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return refresh.access_token


# this class is customized login
class ObtainAuthToken_Customized(ObtainAuthToken):
    serializer_class = CustomeAuthTokenSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id, "email": user.email})


# this class is customized logout
class AuthDiscardedToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # simply delete the token to force a login
        if hasattr(request.user, "auth_token"):
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"detail": "you do not log in"}
            )


# this class is customized reset password
class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data["email"]
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if not user:
            return Response(
                {"error": "User with credentials not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            reset.save()
            reset_url = settings.PASSWORD_RESET_BASE_URL + token
            data = {
                "subject": "this email for reset password",
                "name": get_object_or_404(Profile, user=user),
                "message": "plase click this linl for reseting password" + reset_url,
            }

            Email_obj = EmailMessage(
                "email/reset_password.tpl", data, from_email, to=[email]
            )
            EmailThread(Email_obj).start()
            return Response(
                {"success": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )


# this class for resting passwork when click the links
class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        new_password = data["new_password"]
        confirm_password = data["confirm_password"]

        if new_password != confirm_password:
            return Response(
                {"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST
            )

        reset_obj = PasswordReset.objects.filter(token=token).first()
        if not reset_obj:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = CustomUser.objects.filter(email=reset_obj.email).first()
        if not user:
            return Response(
                {"error": "No user found"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            user.set_password(request.data["new_password"])
            user.save()

            reset_obj.delete()
            return Response(
                {"success": "Password updated"}, status=status.HTTP_205_RESET_CONTENT
            )


# this class for changing password
class ChangePasswordView(generics.UpdateAPIView):

    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = ChangePasswordSerializer


# this class for custimized JWT
class CustimizedTokenObtainPairView(TokenObtainPairView):
    serializer_class = Customized_TOKEN_OBTAIN_PAIR_SERIALIZER


class RequestPasswordResetJWT(generics.GenericAPIView):
    serializer_class = EmailRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = EmailRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj_user = serializer.validated_data["user"]
        token = self.get_token_for_user(obj_user)
        reset_url = settings.PASSWORD_RESET_BASE_URL + str(token)
        data = {
            "subject": "this email for reset password",
            "name": get_object_or_404(Profile, user=obj_user),
            "message": "plase click this linl for reseting password" + str(reset_url),
        }
        Email_obj = EmailMessage(
            "email/reset_password.tpl",
            data,
            from_email,
            to=[serializer.validated_data["email"]],
        )
        EmailThread(Email_obj).start()
        return Response("email send")

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return refresh.access_token


# class for activation of accuounts after registerations
class ActivationAccountJWT(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            # decode toke -> id user
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError as e:

            # check_expired_data
            data = {"detail": str(e)}
            return Response(data=data, status=status.HTTP_410_GONE)
        except jwt.exceptions.InvalidSignatureError as e:
            data = {"detail": str(e)}
            return Response(data=data, status=status.HTTP_410_GONE)
        # user_obj
        user_id = decoded_token["user_id"]
        user_obj = get_object_or_404(CustomUser, id=user_id)
        #   CHECK USER_obj is none
        if user_obj.is_verified:
            data = {"detail": "your account has been already verified"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        # is_varified trun to true
        user_obj.is_verified = True
        user_obj.save()
        data = {"detail": "your account is verfied and activated successfully"}
        return Response(data=data, status=status.HTTP_200_OK)


# this class for resend accounts
class ResendActivationAccountJWT(generics.GenericAPIView):
    serializer_class = EmailRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get("email")
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        if not user_obj.is_verified:
            token = self.get_token_for_user(user_obj)
            reset_url = settings.PASSWORD_ACTIVE_BASE_URL + str(token)
            data = {
                "subject": "this email resend  for activation for accounts",
                "message": "plase click this linl for activation of account "
                + "<br/> "
                + str(reset_url),
            }
            Email_obj = EmailMessage(
                "email/activation_accounts.tpl", data, from_email, to=[user_obj.email]
            )
            EmailThread(Email_obj).start()

            return Response(data={"detail": "email send"}, status=status.HTTP_200_OK)
        else:
            data = {"detail": "your account has been already verified"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return refresh.access_token
