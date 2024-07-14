from django.urls import path
from django.urls import include
from ..views import *

urlpatterns = [
    path("", include("accounts.api.v1.urls.accounts")),
    path("profile", include("accounts.api.v1.urls.profile")),
]
