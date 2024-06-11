from django.db import models
from accounts.models import Profile
# Create your models here.
class Post(models.Model):
    id= models.IntegerField(primary_key=True)
    author = models.ForeignKey(Profile,on_delete= models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=250)
    body = models.TextField()
    img = models.ImageField(blank=True, null=True)
    category = models.ForeignKey("Category", on_delete= models.SET_NULL,null=True, blank=True)
    title = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    created_date = models.DateField()
    updated_date = models.DateField()
    
class Category(models.Model):
    id= models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)