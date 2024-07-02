from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
""" class custom user which based on  AbstractBaseUser"""


class CustomUser(AbstractBaseUser, PermissionsMixin):

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


"""class profile model"""


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, related_name="User", on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=250)
    last_name = models.CharField(_("last name"), max_length=250)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
