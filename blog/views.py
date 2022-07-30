from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .forms import CreatePost
from django.urls import reverse
from django.contrib.auth.models import User

# Function based ListView
def home(request):
    context  = {'posts' : Post.objects.all()}
    return render(request, 'blog/index.html', context)

# Class based ListView
class home(ListView):
    model = Post
    context_object_name = "posts"
    ordering = ["-date"]
    paginate_by = 3

class UserPost(ListView):
    model = Post
    context_object_name = "posts"
    ordering = ["-date"]
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by("-date")

# Class based DetailView
class PostDetail(DetailView):
    model = Post

# Function based DetailView
def Detail(request,pk):
    object = Post.objects.get(id = pk)
    return render(request,"blog/post_detail.html",{
        "object" : object
    } )

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def Create(request):
    if request.method == "POST":
        c_form = CreatePost(request.POST)
        c_form.instance.author = request.user   # we can take any instance of a form by using this method
        if c_form.is_valid():
            c_form.save()
        return redirect("blog-home")

    else:
        c_form = CreatePost()

    return render(request, 'blog/create.html', {'c_form' : c_form})
    


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def UpdatePost(request, pk):
    obj = get_object_or_404(Post, id=pk)
    if obj.author == request.user:
        if request.method == "POST":
            form = CreatePost(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect(reverse("post-detail",kwargs={"pk":pk}))
        else:
            form = CreatePost(instance = obj)

        return render(request,"blog/post_form.html",{
            "form": form
        })
    else:
        return HttpResponse("<h1>You can't update other user's content.</h1>")




class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def DeletePost(request,pk):
    obj = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('blog-home')
    else:
        return render(request,"blog/post_confirm_delete.html",{
            "object" : obj
        })

def about(request):
    return render(request, 'blog/about.html', {'title' : 'Blog1'})