from django.views import generic
from django.shortcuts import redirect, get_object_or_404, render  # Added render
from django.urls import reverse
from rest_framework import viewsets
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Comment
from .forms import CommentForm, NewUserForm  # Import both forms
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



@login_required
def add_comment(request, slug):
    """Handle comment submission - only for logged-in users"""
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  
            comment.save()
            messages.success(request, "Your comment has been added!")
            return redirect('blog:post_detail', slug=slug)
        else:
            messages.error(request, "Error adding comment. Please try again.")
            return redirect('blog:post_detail', slug=slug)
    
    return redirect('blog:post_detail', slug=slug)
def delete_comment(request, pk):
    """Handle comment deletion"""
    comment = get_object_or_404(Comment, pk=pk)
    post_slug = comment.post.slug
    
    if request.method == 'POST':
        comment.delete()
    
    return redirect('blog:post_detail', slug=post_slug)

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('blog:home')  
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'register.html', {"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('blog:home')  
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', {"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('blog:home')  