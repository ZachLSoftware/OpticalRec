from django.shortcuts import render, redirect
from .models import Video
from .forms import VideoForm
from pathlib import Path


# Create your views here.
def index(request):
    return render(request, "index.html")


def video_upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            object = form.save(commit=False)
            if request.user.is_authenticated:
                object.userId=request.user.id
            else:
                object.userId=0
            object.save()
            return redirect('index')
    else:
        form = VideoForm()
    return render(request, 'video_upload.html', {
        'form': form
    })

def list_videos(request):
    vids=Video.objects.filter(userId=0).order_by('-uploadedAt')
    return render(request, 'vid_list.html', {'vids':vids})

def delete_video(request, vid_id):
    obj=Video.objects.get(id=vid_id)
    obj.delete()
    return redirect(list_videos)