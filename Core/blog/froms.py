from django import forms
from .models import Post,Category

# Form for Model Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "category", "status"]