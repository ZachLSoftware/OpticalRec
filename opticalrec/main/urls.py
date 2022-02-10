from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.video_upload, name='video_upload'),
    path('list', views.list_videos, name='list_videos'),
    path('framelist', views.framelist, name='framelist'),
    path('delete_video/<int:vid_id>', views.delete_video, name='delete_video'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('import_video_tensor/<int:vid_id>', views.import_video_tensor, name='import_video_tensor')
]