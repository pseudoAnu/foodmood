from django import forms
from .models import Post,Comment

class PostModelForm(forms.ModelForm):
    content=forms.CharField(widget=forms.Textarea(attrs={'rows':2,'placeholder':"What's on your mind?",'style':"padding: 10px;margin-left: 28px;margin-top: 18px; border-radius: 21px;width: 87%; background-color: gainsboro;"}))
    class Meta:
        model=Post
        fields=['content','image']
class CommentModelForm(forms.ModelForm):
    body=forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Add a comment...','autocomplete':'off','style':"margin-left: 5px;"}))
    class Meta:
        model=Comment
        fields=('body',)
