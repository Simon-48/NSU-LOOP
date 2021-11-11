from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    """
    This class takes a helper class ModelForm that 
    lets you create a Form class from a Django model.
	"""
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Post
        fields = ('content', 'image')

class CommentModelForm(forms.ModelForm):
    """
    This class takes a helper class ModelForm that 
    lets you create a Form class from a Django model.
	"""
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = Comment
        fields = ('body',)