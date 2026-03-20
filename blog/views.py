from django.views import generic
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import Post, Comment
from .forms import CommentForm

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


def add_comment(request, slug):
    """Handle comment submission"""
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=slug)
    
    return redirect('post_detail', slug=slug)


def delete_comment(request, pk):
    """Handle comment deletion"""
    comment = get_object_or_404(Comment, pk=pk)
    post_slug = comment.post.slug
    
    if request.method == 'POST':
        comment.delete()
    
    return redirect('post_detail', slug=post_slug)
