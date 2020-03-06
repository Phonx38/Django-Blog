from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blogApp/home.html'
    context_object_name = 'posts'

def about(request):
    return render(request,'about.html', {'title':'About'})