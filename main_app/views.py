from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like, Bookmark
from .forms import PostForm, CommentForm

def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {'posts': posts})

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
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})

@login_required
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
    return render(request, 'comments/add.html', {'form': form, 'post': post})

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
    return redirect('posts_list')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def plants_index(request):
    posts = Post.objects.all()
    return render(request, 'plants/index.html', {'posts': posts})

# def plants_index(request):
#     return render(request, 'plants/index.html', {
#         'plants': plants
#     })
