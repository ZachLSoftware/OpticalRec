from django.shortcuts import render, redirect
from .models import Video
from .models import Frame
from .forms import VideoForm
from pathlib import Path
from .utils.Upload import videoIntoFrames
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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
    vids=Video.objects.filter(user_id=0).exclude(videoFile="Deleted").order_by('-uploadedAt')
    return render(request, 'vid_list.html', {'vids':vids})

def delete_video(request, vid_id):
    obj=Video.objects.get(id=vid_id)
    obj.delete()
    return redirect(list_videos)


def dashboard(request):

    return render(request,"dashboard.html")

def import_video_tensor(request, vid_id):
    obj=Video.objects.get(id=vid_id)
    videoIntoFrames(obj)
    return redirect(list_videos)


def framelist(request):
    frames=Frame.objects.all()
    return render(request,"frame_list.html", {"frames":frames})

def profile(request):
    return render(request, 'profile.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username}'s account created.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})