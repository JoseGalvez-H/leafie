from django import forms
from .models import Post
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content'] 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        # widgets = {
        #     'content': forms.Textarea(attrs={'cols': 40, 'rows': 5}) 
        # }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        