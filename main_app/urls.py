from django.urls import path
from .import views

urlpatterns = [
    path('', views.home),
    path('about/', views.about, name='about'),
    path('plants/', views.posts_list),
    path('posts/', views.posts_list, name='posts_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('post/like/<int:post_id>/', views.like_post, name='like_post'),
    path('post/<int:post_id>/bookmark/', views.bookmark_post, name='bookmark_post'),
    path('bookmarked/', views.bookmarked_posts, name='bookmarked_posts'),
    path('post/create/', views.post_create, name='post_create'),
]
