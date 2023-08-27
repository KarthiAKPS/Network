from django import forms
from django.http import request
from django.forms import ModelForm
from .models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('content','liked', 'creater')
        widgets = {
            'content' : forms.Textarea(attrs={'placeholder':'Write your mind here...','class':'form-control', 'rows':'3'}),
            'liked' : forms.HiddenInput(),
            'creater' : forms.HiddenInput(),
        }
        labels = {
            'content' : ''
        }
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creater'].required = False