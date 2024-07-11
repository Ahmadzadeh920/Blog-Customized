from django.urls import path
from django.urls import include
from rest_framework.authtoken.views import ObtainAuthToken
from . import views
# simple JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'api_v1'
urlpatterns = [ 
    #registeration
    path('registration/',views.RegisterationApiview.as_view(),name='registeration'),
    #login token
    #with ObtainAuthToken token is generated but we can not logout and destroy token
     path('token/login/',ObtainAuthToken.as_view(), name = "Token_login"),
     # customized ObtainAuthToken
    path('token/login/customized/',views.ObtainAuthToken_Customized.as_view(), name = "Token_login_customized"),
    #login jwt
    #logout
    path('token/logout/',views.AuthDiscardedToken.as_view(), name = "Token_logout"),
    
    #reset password
    path('token/reset/request/',views.RequestPasswordReset.as_view(), name = "Token_reset_password_request"),
    path('token/reset/',views.ResetPassword.as_view(), name = "Token_reset_password"),
    # change password
     path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='auth_change_password'),
    #simple JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
     #customized simple JWT
     path('api/token/customized', views.CustimizedTokenObtainPairView.as_view(), name='token_obtain_pair_customized'),
     
     # Profile
    path('[profile/]', views.ProfileAPIView.as_view(), name='profile_api_view'),

]