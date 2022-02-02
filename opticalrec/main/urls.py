from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.video_upload, name='video_upload'),
]