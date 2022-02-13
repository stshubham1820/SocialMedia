from django.forms import ModelForm
from .models import Post , UserBio

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', ]
class UserBioForm(ModelForm):
    class Meta:
        model = UserBio
        exclude = ['id','friends',]