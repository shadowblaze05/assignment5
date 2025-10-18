from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib import messages
from pages.models import Post
from pages.forms import PostForm
from django.shortcuts import redirect
from django.shortcuts import render
from django import forms
from .models import Comment




# Create your views here.
def home(request):
    ctx = {"title": "Home", "features": ["Django", "Templates", "Static files"]}
    return render(request, "home.html", ctx)

def about(request):
    return render(request, "about.html", {"title": "About"})

def hello(request, name):
    return render(request, "hello.html", {"name": name})

def gallery(request):
    # Assume images placed in pages/static/img/
    images = ["img1.jpg", "img2.jpg", "img3.jpg"]
    return render(request, "gallery.html", {"images": images})

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def server_error_view(request):
    return render(request, '500.html', status=500)

def post_list(request):
    # Model.objects.all()
    posts = Post.objects.all().prefetch_related('comments')
    context = {
        'posts': posts,
        'title': 'Posts',
    }
    return render(request, 'post_list.html', context)

def admin(request):
    return redirect('/admin/')

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New post created')
            return redirect('post_list')
        messages.error(request, 'Get Better!')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

def post_view(request, pk):
    #post = get_object_or_404(Post, pk=pk)
    post = Post.objects.get(pk=pk)
    comments = Post.objects.prefetch_related('comments')
    return render(request, 'post_view.html', {'post': post})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'New post created')
            return redirect('post_list')
        messages.error(request, 'Get Better!')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, f"Goodbye {post.title} ")
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your comment'}),
        }

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=slug)  # refresh page after comment
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

def add_comment(request, post_slug):
    """
    Accept POST for adding a comment. On success redirect back to post detail.
    On validation error, re-render post_detail with the filled form and errors.
    """
    post = get_object_or_404(Post, slug=post_slug, status='published')
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(post.get_absolute_url() + '#comments')
    comments = post.comments.filter(active=True)
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

def csrf_failure(request, reason=""):
    return render(request, '403_csrf.html', {'reason': reason}, status=403)

