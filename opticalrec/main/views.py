from django.shortcuts import render, redirect
from .models import Video
from .models import Frame
from .forms import *
from pathlib import Path
from .utils.Upload import videoIntoFrames
from .utils.preview_frame import preview_frame
from main.models import Frame
from django.urls import reverse
from opticalrec.settings import MEDIA_ROOT
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
import os
import cv2
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "index.html")

@login_required
def video_upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            object = form.save(commit=False)
            if request.user.is_authenticated:
                object.user=request.user
            object.save()
            return redirect(reverse('video_crop_display', kwargs={"vid_id":object.id}))
    else:
        form = VideoForm()
    return render(request, 'video_upload.html', {
        'form': form
    })

@login_required
def list_videos(request):
    vids=Video.objects.filter(user=request.user).exclude(videoFile="Deleted").order_by('-uploadedAt')
    return render(request, 'vid_list.html', {'vids':vids})

@login_required
def delete_video(request, vid_id):
    obj=Video.objects.get(id=vid_id)
    obj.delete()
    return redirect(list_videos)

@login_required
def dashboard(request):

    return render(request,"dashboard.html")

@login_required
def import_video_tensor(request, vid_id):
    obj=Video.objects.get(id=vid_id)
    videoIntoFrames(obj)
    return redirect(list_videos)

@login_required
def framelist(request):
    frames=Frame.objects.all()
    return render(request,"frame_list.html", {"frames":frames})

@login_required
def video_crop_display(request, vid_id):
    obj=Video.objects.get(id=vid_id)
    if request.method == 'POST':
        form = VideoResizeForm(request.POST, request.FILES)
        if form.is_valid():
            object = form.save(commit=False)
            object.video=obj
            object.x2=(object.x1+object.width)/object.nat_width
            object.y2=(object.y1+object.height)/object.nat_height
            object.x1=object.x1/object.nat_width
            object.y1=object.y1/object.nat_height
            object.save()
            response = {'status': 0, 'url':"/main/import_video_tensor/"+str(obj.id), 'message': ("succesful")}
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            response = {'status': 1, 'message': ("Issue Processing Form")}
            return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        form = VideoResizeForm()
        f=preview_frame(obj)
    
        return render(request, 'video_crop.html', {'frame':f, 'form':form})

def profile(request):
    return render(request, 'profile.html')


def register(request):
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username}'s account created.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
