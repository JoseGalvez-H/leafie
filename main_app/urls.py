from django.urls import path, include
from .import views
from .views import home
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('', views.home),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('plants/', views.posts_list),
    path('posts/', views.posts_list, name='posts_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('post/like/<int:post_id>/', views.like_post, name='like_post'),
    path('post/<int:post_id>/bookmark/', views.bookmark_post, name='bookmark_post'),
    path('bookmarked/', views.bookmarked_posts, name='bookmarked_posts'),
    path('post/create/', views.post_create, name='post_create'),
    # path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
]
