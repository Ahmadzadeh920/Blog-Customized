from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


from ....models import CustomUser, Profile

class Profile_Serializer(serializers.ModelSerializer):
    email = serializers.CharField(source = 'user.email')
    
    class Meta:
        model = Profile
        fields = ['id', 'email' , 'first_name', 'last_name' , 'image', 'description']
        
        
       