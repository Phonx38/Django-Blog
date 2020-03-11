from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post
import django.core.mail

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by= 4

class UserPostListView(ListView):
    model = Post
    template_name = 'user_post.html'
    context_object_name = 'posts'
    
    paginate_by= 2

    def get_queryset(self):
        user = get_object_or_404(User,username =self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin,LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
         post = self.get_object()
         if self.request.user == post.author:
             return True
         return False

class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
         post = self.get_object()
         if self.request.user == post.author:
             return True
         return False

def about(request):
    return render(request,'about.html', {'title':'About'})