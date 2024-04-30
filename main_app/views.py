from django.shortcuts import render, redirect, get_object_or_404
import os
from .models import Post, Comment, Like, Bookmark
from .forms import PostForm, CommentForm
import requests

def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})


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

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        return redirect('posts_list')
    return redirect('posts_list')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    return render(request, 'posts/detail.html', {'post': post, 'comments': comments})


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


def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk =comment_id, post_id=post_id, author=request.user)
    comment.delete()
    return redirect('post_detail', pk=post_id)


def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete() 
    return redirect('posts_list')


def bookmark_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    bookmark, created = Bookmark.objects.get_or_create(post=post, user=request.user)
    if not created:
        bookmark.delete() 
    return redirect('bookmarked_posts')


def bookmarked_posts(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('post')
    posts = [bookmark.post for bookmark in bookmarks]
    return render(request, 'posts/bookmarked_posts.html', {'posts': posts})


def home(request):
    return render(request, 'home.html')

def about(request):
    API_KEY = os.environ.get('API_KEY')
    query = request.GET.get('q')
    url = f'https://perenual.com/api/species-list?key={API_KEY}'
    
    if query:
        url += f'&q={query}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        plants = data.get('data', [])
        plant = plants[0] if plants else None
    except requests.RequestException as e:
        plant = None
        print(f"API request failed: {e}")
    except ValueError:
        plant = None
        print("Error decoding JSON from API")
    return render(request, 'about.html', {'plant': plant})
