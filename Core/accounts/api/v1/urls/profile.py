from django.urls import path
from django.urls import include
from ..views import profile as views

urlpatterns = [ 
 path('', views.ProfileAPIView.as_view(), name='profile_api_view'),
]
 