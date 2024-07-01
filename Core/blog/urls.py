from django.urls import path
from django.conf import settings
from django.urls import include
from django.views.generic import RedirectView
from . import views
app_name = "blog"

urlpatterns = [
    # path template view for index
    path( '', views.IndexView.as_view() , name= "Index"),
    # path for redirect to my personal github account
    path(
        "private_website/",RedirectView.as_view(url="https://ahmadzadeh920.github.io/"),name="go-to-private_website" ),
    # this urls for the list of blogs
    path( 'list/', views.PostListView.as_view() , name= "ListPostView"),
   #this urls for details of posts 
    path( 'list/<int:pk>/', views.PostDetailView.as_view() , name= "DetailPostView"),
    # this Url for Creating new posts
    path( 'create/', views.PostCreateView.as_view() , name= "PostCreateView"),
   # this Url for edit Post 
   path("list/<int:pk>/edit/", views.PostEditView.as_view(), name="PostEditView"),

   # this Url for deete Post 
   path("list/<int:pk>/delete/", views.PostDeleteView.as_view(), name="PostDeleteView"),
]
