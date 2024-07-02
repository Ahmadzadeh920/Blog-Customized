from django.contrib import admin
from .models import Post, Category


# Register your models here.
class AdminPost(admin.ModelAdmin):
    list_display = [
        "author",
        "title",
        "category",
        "status",
        "created_date",
        "updated_date",
    ]


admin.site.register(Post, AdminPost)
admin.site.register(Category)
