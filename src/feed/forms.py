from django import forms
from .models import ImagePost, Post


class ImagePostForm(forms.ModelForm):
    class Meta:
        model = ImagePost
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'custom-file-input'})
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'custom-file-input'}),
        }
