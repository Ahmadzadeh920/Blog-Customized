from django.urls import path, include
from rest_framework.documentation import include_docs_urls

from rest_framework.routers import DefaultRouter

from . import views

app_name = "api-v1"

urlpatterns = [
    path("post/", views.PostList.as_view(), name="post-list"),
    path("post/<int:pk>/", views.PostDetail.as_view(), name="post-detail"),
]
router = DefaultRouter()
# router.register("post", views.PostViewSet, basename="post")
router.register("ModelPost", views.PostModelViewSet, basename="model_post")

urlpatterns += router.urls
