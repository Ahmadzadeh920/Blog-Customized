from django.urls import path
from django.urls import include
import djoser
from . import views


app_name = "accounts"

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("all_auth/", include("allauth.urls")),
    path("", include("django.contrib.auth.urls")),
    path("api/v1/", include("accounts.api.v1.urls")),
    path("api/v2/", include("djoser.urls")),
    path("api/v2/", include("djoser.urls.jwt")),
    path("email_celery/", views.send_email, name = "send_email" ),
]
