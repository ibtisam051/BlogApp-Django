from django.views import generic
from django.shortcuts import redirect, get_object_or_404, render  # Added render
from django.urls import reverse
from django.http import HttpResponse
from rest_framework import viewsets
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Comment
from .forms import CommentForm, NewUserForm  # Import both forms
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(600), name='dispatch')
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


@method_decorator(cache_page(300), name='dispatch')
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()

        session = self.request.session
        session['last_viewed_post'] = self.object.title
        session['last_viewed_slug'] = self.object.slug
        session['viewed_posts_count'] = session.get('viewed_posts_count', 0) + 1
        session['session_user_status'] = 'authenticated' if self.request.user.is_authenticated else 'anonymous'

        context['session_info'] = {
            'last_post': session.get('last_viewed_post'),
            'count': session.get('viewed_posts_count'),
            'user_status': session.get('session_user_status'),
        }
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


def cookie_session(request):
    request.session.set_test_cookie()
    return HttpResponse(
        "<h1>dataflair</h1>"
        "<p>Test cookie has been set. Now visit /deletecookie/ to verify browser cookie support.</p>"
    )


def cookie_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        return HttpResponse(
            "<h1>dataflair</h1>"
            "<p>Cookie accepted by browser.</p>"
        )
    return HttpResponse(
        "<h1>dataflair</h1>"
        "<p>Your browser does not accept cookies.</p>"
    )


def create_session(request):
    request.session['name'] = 'username'
    request.session['password'] = 'password123'
    return HttpResponse(
        "<h1>dataflair</h1>"
        "<p>Session variables have been created.</p>"
    )


def access_session(request):
    if not request.session.get('name') and not request.session.get('password'):
        return redirect('blog:create_session')

    response = "<h1>Welcome to Sessions of dataflair</h1><br>"
    response += f"Name : {request.session.get('name')} <br>"
    response += f"Password : {request.session.get('password')} <br>"
    return HttpResponse(response)


def delete_session(request):
    request.session.pop('name', None)
    request.session.pop('password', None)
    return HttpResponse(
        "<h1>dataflair</h1>"
        "<p>Session data cleared from the database.</p>"
    )


def flush_session(request):
    request.session.flush()
    return HttpResponse(
        "<h1>dataflair</h1>"
        "<p>Session flushed and session cookie removed.</p>"
    )


def session_status(request):
    session = request.session
    session['session_visits'] = session.get('session_visits', 0) + 1

    context = {
        'user_status': request.user.username if request.user.is_authenticated else 'Anonymous',
        'is_authenticated': request.user.is_authenticated,
        'viewed_posts_count': session.get('viewed_posts_count', 0),
        'last_viewed_post': session.get('last_viewed_post'),
        'session_visits': session.get('session_visits', 0),
    }
    return render(request, 'session_status.html', context)


def clear_session(request):
    for key in [
        'last_viewed_post',
        'last_viewed_slug',
        'viewed_posts_count',
        'session_user_status',
        'session_visits',
        'name',
        'password',
    ]:
        request.session.pop(key, None)
    messages.info(request, 'Session demo data cleared.')
    return redirect('blog:session_status')


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