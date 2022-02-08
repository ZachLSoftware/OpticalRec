from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.video_upload, name='video_upload'),
    path('list', views.list_videos, name='list_videos'),
    path('delete_video/<int:vid_id>', views.delete_video, name='delete_video')
]