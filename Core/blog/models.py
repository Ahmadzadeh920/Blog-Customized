from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse

# Get user model
User = get_user_model()


# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    body = models.TextField()
    img = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.BooleanField(default=False)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
    
    # this function is called for fields snippets
    def get_snippet(self):
        # get the full text you want to create a snippet from
        full_text = self.body  # replace field_name with the actual field name containing the text
        
        # define the number of words to include in the snippet
        word_limit = 20
        
        # split the full text into words
        words = full_text.split()
        # create the snippet from the first few words
        snippet = ' '.join(words[:word_limit])
        return snippet
    def get_absolute_api_url(self):
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.id})


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
