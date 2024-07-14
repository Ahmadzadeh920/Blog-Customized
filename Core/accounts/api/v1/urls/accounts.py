from django.urls import path
from django.urls import include
from rest_framework.authtoken.views import ObtainAuthToken
from ..views import accounts as views

# simple JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "api_v1"
urlpatterns = [
    # registeration with jwt
    path("registration/", views.RegisterationApiview.as_view(), name="registeration"),
    # login token
    # with ObtainAuthToken token is generated but we can not logout and destroy token
    path("token/login/", ObtainAuthToken.as_view(), name="Token_login"),
    # customized ObtainAuthToken
    path(
        "token/login/customized/",
        views.ObtainAuthToken_Customized.as_view(),
        name="Token_login_customized",
    ),
    # logout
    path("token/logout/", views.AuthDiscardedToken.as_view(), name="Token_logout"),
    # reset password
    path(
        "token/reset/request/",
        views.RequestPasswordReset.as_view(),
        name="Token_reset_password_request",
    ),
    path(
        "token/reset/<str:token>/",
        views.ResetPassword.as_view(),
        name="Token_reset_password",
    ),
    # change password
    path(
        "change_password/<int:pk>/",
        views.ChangePasswordView.as_view(),
        name="auth_change_password",
    ),
    # simple JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # customized simple JWT
    path(
        "api/token/customized",
        views.CustimizedTokenObtainPairView.as_view(),
        name="token_obtain_pair_customized",
    ),
    # activation user with JWT authentication
    path("confirm/", views.ChangePasswordView.as_view(), name="auth_change_password"),
    # resend activation with JWT authentication
    path(
        "resend_activation/",
        views.ChangePasswordView.as_view(),
        name="auth_change_password",
    ),
    # Reset password with JWT authentication
    path(
        "token/reset/request/jwt",
        views.RequestPasswordResetJWT.as_view(),
        name="Token_reset_password_request_jwt",
    ),
    # this url for activate accounts after registeration
    path(
        "activate/jwt/<str:token>",
        views.ActivationAccountJWT.as_view(),
        name="activation_account_jwt",
    ),
    path(
        "activate/jwt/resend/",
        views.ResendActivationAccountJWT.as_view(),
        name="resend_activation_account_jwt",
    ),
]
