from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from taggit.forms import TagField, TagWidget
from .models import Profile, Post, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address already in use.")
        return email
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','prof_pic']
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class PostForm(forms.ModelForm):
    class Meta:
        tags = TagField(widget=TagWidget())
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Add tags separated by commas'})
        }
        