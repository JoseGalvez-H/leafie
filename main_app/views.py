from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Like, Bookmark
from .forms import PostForm, CommentForm
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth import logout
import requests, random
import os

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts_list') 
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'posts/detail.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        return redirect('posts_list')
    else:
        return redirect('posts_detail', pk=pk)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post_id)
    else:
        form = CommentForm()
    return render(request, 'posts/comments/add.html', {'form': form, 'post': post})

@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk =comment_id, post_id=post_id, author=request.user)
    comment.delete()
    return redirect('post_detail', pk=post_id)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete() 
    return redirect('posts_list')

@login_required
def bookmark_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    bookmark, created = Bookmark.objects.get_or_create(post=post, user=request.user)
    if not created:
        bookmark.delete() 
    return redirect('bookmarked_posts')

@login_required
def bookmarked_posts(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('post')
    posts = [bookmark.post for bookmark in bookmarks]
    return render(request, 'posts/bookmarked_posts.html', {'posts': posts})


def home(request):
    return render(request, 'home.html')

@login_required
def about(request):
    API_KEY = os.environ.get('API_KEY')
    query = request.GET.get('q')
    url = f'https://perenual.com/api/species-list?key={API_KEY}'
    if query:
        url += f'&q={query}'
    else:
        url += '&random=true'  
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        plants = data.get('data', [])
        if not query and plants:
            plant = random.choice(plants) 
        else:
            plant = plants[0] if plants else None
    except requests.RequestException as e:
        plant = None
        print(f"API request failed: {e}")
    except ValueError:
        plant = None
        print("Error decoding JSON from API")
    return render(request, 'about.html', {'plant': plant})

