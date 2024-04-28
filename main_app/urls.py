from django.urls import path
from .import views

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('plants/', views.plants_index),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/', views.posts_list, name='posts_list'),
]
