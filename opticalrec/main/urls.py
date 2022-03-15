from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.video_upload, name='video_upload'),
    path('list', views.list_videos, name='list_videos'),
    path('framelist', views.framelist, name='framelist'),
    path('delete_video/<int:vid_id>', views.delete_video, name='delete_video'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('import_video_tensor/<int:vid_id>/<str:label>', views.import_video_tensor, name='import_video_tensor'),
    path('video_crop_display/<int:vid_id>', views.video_crop_display, name='video_crop_display'),
    path('video_crop_display/<int:vid_id>/<int:frame_num>', views.video_crop_display, name='video_crop_display'),
    path('profile', views.profile, name = 'profile'),
    path('login', auth_views.LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('logout', auth_views.LogoutView.as_view(template_name = 'logout.html'), name = 'logout'),
    path('register', views.register, name = 'register'),
    path('extract_data/<int:label_id>', views.extractData, name= 'extract_data'),

]