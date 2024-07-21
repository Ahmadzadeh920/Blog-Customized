from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from ....models import Profile
from ..serializers import Profile_Serializer


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = Profile_Serializer
    query_set = Profile.objects.all()
    permission_class = [IsAuthenticated]
    
    
    def get_object(self):
        obj = get_object_or_404(self.query_set, user=self.request.user)
        return obj
    
    
    # with this method, all views is stored in the cache
    @method_decorator(cache_page(60*10))
    def dispatch(self, *args, **kwargs):
        return super(ProfileAPIView, self).dispatch(*args, **kwargs)
