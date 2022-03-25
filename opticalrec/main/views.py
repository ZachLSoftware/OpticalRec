from django.shortcuts import render, redirect
from .models import *
from forms import *
from pathlib import Path
from utils.Upload import videoIntoFrames
from utils.preview_frame import preview_frame
from utils.predict_data import eval_data
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
import csv

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
    context={}
    vids=Video.objects.filter(user=request.user).exclude(videoFile="Deleted").order_by('-uploadedAt')
    context['videos']=vids
    labels=[]
    for vid in vids:
        labels+=Label.objects.filter(video_id=vid.id)
    context['labels']=labels
    return render(request, 'vid_list.html', context)

@login_required
def delete_video(request, vid_id):
    obj=Video.objects.get(id=vid_id)
    obj.delete()
    return redirect(list_videos)

@login_required
def dashboard(request):
    context={
        'videos': {} 
    }
    unsortedData = ExtractedData.objects.filter(user=request.user).order_by('-video_id')
    videos={}
    for data in unsortedData:
        if data.video_id not in videos:
            videos[data.video_id]=[]
        if not videos[data.video_id]:
            videos[data.video_id].append({data.label.name: []})
        else:
            label_test=False 
            for vid in videos[data.video_id]:
                if data.label.name in vid:
                    label_test=True
                    break
            if not label_test:
                videos[data.video_id].append({data.label.name:[]})

    for vid in videos.keys():
        for data in unsortedData:
            if data.video_id==vid:
                for l in videos[vid]:
                    for label in l.keys():
                        if data.label.name==label:
                            l[label].append(data)
    for vid in videos.keys():
        context['videos'][vid]=Video.objects.get(id=vid).name
    context['data']=videos
    return render(request,"dashboard.html", context)

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
def video_crop_display(request, vid_id, frame_num=0, finish=0):
    obj=Video.objects.get(id=vid_id)
    if request.method == 'POST':
        form = VideoResizeForm(request.POST, request.FILES)
        if form.is_valid():
            object = form.save(commit=False)
            object.video=obj
            if Label.objects.filter(video_id=object.video_id).filter(name=object.label).exists():
                response = {'status': 1, 'message': ("A label of this type already exists for this video")}
                return HttpResponse(json.dumps(response), content_type='application/json')
            object.x2=(object.x1+object.width)/object.nat_width
            object.y2=(object.y1+object.height)/object.nat_height
            object.x1=object.x1/object.nat_width
            object.y1=object.y1/object.nat_height
            lab=Label()
            lab.name=object.label
            lab.video=obj
            lab.save()
            object.save()
            if finish==1:
                response = {'status': 0, 'url':"/main/import_video_tensor/"+str(obj.id), 'message': ("succesful")}
                return HttpResponse(json.dumps(response), content_type='application/json')
            else:
                response = {'status': 0, 'url':"/main/video_crop_display/" + str(vid_id) + '/' + str(frame_num), 'message': ("succesful")}
                return HttpResponse(json.dumps(response), content_type='application/json')

        else:
            response = {'status': 1, 'message': ("Issue Processing Form")}
            return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        form = VideoResizeForm()
        if frame_num!=0:
            Frame.objects.get(video_id=obj.id, frameFile__contains="previewFrame").delete()
            frame_num+=50
        else:
            frame_num=0
        f=preview_frame(obj,frame_num)
    
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

def extractAllData(request, vid_id):
    labels=Label.objects.filter(video_id=vid_id)
    for label in labels:
        if(not ExtractedData.objects.filter(label_id=label.id).exists()):
            eval_data(label.id)
    return redirect(dashboard)


def extractData(request, label_id):
    if(not ExtractedData.objects.filter(label_id=label_id).exists()):
        eval_data(label_id)
    return redirect(dashboard)

def exportToCSV(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Video','Frame','User','Label','Timestamp','Value', 'Difference'])

    for data in ExtractedData.objects.all().values_list('video','frame','user','label','timeStamp','value','valueChange'):
        writer.writerow(data)

    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    return response
