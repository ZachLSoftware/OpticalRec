from django import forms
from .models import Video, videoResize

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('name', 'videoFile', )

class VideoResizeForm(forms.ModelForm):
    class Meta:
        model = videoResize
        fields = ('label', 'x1', 'y1', 'width', 'height', 'nat_height', 'nat_width',)