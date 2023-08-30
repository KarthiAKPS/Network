from django import forms
from django.http import request
from django.forms import ModelForm
from .models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('content','liked', 'creater', 'image')
        widgets = {
            'content' : forms.Textarea(attrs={'placeholder':'Write your mind here...','class':'form-control', 'rows':'3'}),
            'liked' : forms.HiddenInput(),
            'creater' : forms.HiddenInput(),
            'image' : forms.FileInput(attrs={'class':'form-control-file', 'style':'margin : 0 10px 0'}),
        }
        labels = {
            'content' : '',
            'image' : ''
        }
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creater'].required = False