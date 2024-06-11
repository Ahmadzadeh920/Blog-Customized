from django.db import models

# Create your models here.
class Post(models.Model):
    id= models.IntegerField(primary_key=true)
    title = models.CharField(max_length=250)
    body = models.TextField()
    img = models.ImageField(blank=True, null=True)
    category = models.ForeignKey("Category", on_delete=SET_NULL)
    status = models.BooleanField(default=False)
    created_date = models.DateField()
    updated_date = models.DateField()