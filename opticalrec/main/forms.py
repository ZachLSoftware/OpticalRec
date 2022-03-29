from django import forms
from django.forms import ModelForm, TextInput, FileInput
from .models import Label, Video, videoResize
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('name', 'videoFile', )
        widgets = {
            'name': TextInput(attrs={
                'class':'form-control',
                'placeholder':'Video Name'
            }),
            'videoFile': FileInput(attrs={
                'class':'form-control',
                'placeholder':'.mp4, .avi'
            }),
        }

class VideoResizeForm(forms.ModelForm):
    class Meta:
        model = videoResize
        fields = ('label', 'x1', 'y1', 'width', 'height', 'nat_height', 'nat_width',)

class CreateUser(UserCreationForm):
    #password2 = None


    class Meta:
        model = get_user_model()
        fields= ("username",)