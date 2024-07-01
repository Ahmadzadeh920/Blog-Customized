from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView , TemplateView, RedirectView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from django.utils import timezone
from .froms import PostForm

# Create your views here.

# create template class for index
class IndexView(TemplateView):
    template_name = "blog/index.html"
    
    


# this class foe listing Post and return all features related to the post
class PostListView(ListView):
    template_name = "post_list.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 2
    def get_context_data(self, **kwargs: Any):
        context= super().get_context_data(**kwargs)
        context['last_login']= timezone.now()
        return context
    
    
# this class for detail of post objects identified bu pk
class PostDetailView(DetailView):
    model = Post
    context_object_name= "post"



# this class for creating new post
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/list/"
    def form_valid(self, form):
        form.instance.updated_date = timezone.now()
        form.instance.author = self.request.user
        return super().form_valid(form)


# class for Update one post
class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/list/"
    def form_valid(self, form):
        form.instance.updated_date = timezone.now()
        return super().form_valid(form)
    
class PostDeleteView(DeleteView):
    model = Post
    success_url = "/blog/list/"