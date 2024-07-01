from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Get user model 
User = get_user_model()
# Create your models here.
class Post(models.Model):
    id= models.AutoField(primary_key=True)
    author = models.ForeignKey(User,on_delete= models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=250)
    body = models.TextField()
    img = models.ImageField(blank=True, null=True)
    category = models.ForeignKey("Category", on_delete= models.SET_NULL,null=True, blank=True)
    status = models.BooleanField(default=False)
    created_date = models.DateField(default=timezone.now())
    updated_date = models.DateField()
    def __str__(self):
        return self.title
    
class Category(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name