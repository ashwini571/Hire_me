from django import forms
from .models import ImagePost, Post, Comment


class ImagePostForm(forms.ModelForm):
    class Meta:
        model = ImagePost
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'attachment-box ripple-effect'})
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'attachment-box ripple-effect'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
        }
