from django import forms
from .models import Post
from .models import Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
        
    
    def clean_title(self):
        t = self.cleaned_data['title']
        if "test" in t.lower():
            raise forms.ValidationError("Title cannot contain the word 'test'")
        if len(t) < 3:
            raise forms.ValidationError("Title is short like you")
        return t
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your comment'}),
        }