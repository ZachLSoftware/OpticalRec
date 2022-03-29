from django.shortcuts import render, redirect
from matplotlib.style import context
from .models import *
from .forms import *
from pathlib import Path
from .utils.Upload import videoIntoFrames
from .utils.preview_frame import preview_frame
from .utils.predict_data import eval_data
from .utils.template import getTemplate
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
    context={}
    context['template']=getTemplate(request)
    return render(request, "index.html", context)

@login_required
def video_upload(request):
    context={}
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
        context['form']=form
    context['template']=getTemplate(request)
    return render(request, 'video_upload.html', context)

@login_required
def list_videos(request):
    context={}
    vids=Video.objects.filter(user=request.user).exclude(videoFile="Deleted").order_by('-uploadedAt')
    context['videos']=vids
    labels=[]
    for vid in vids:
        labels+=Label.objects.filter(video_id=vid.id)
    context['labels']=labels
    context['template']=getTemplate(request)
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
    context['template']=getTemplate(request)
    return render(request,"dashboard.html", context)

@login_required
def import_video_tensor(request, vid_id):
    obj=Video.objects.get(id=vid_id)
    videoIntoFrames(obj)
    return redirect(list_videos)

@login_required
def framelist(request):
    context={}
    context['template']=getTemplate(request)
    frames=Frame.objects.all()
    context['frames',frames]
    return render(request,"frame_list.html", context)

@login_required
def video_crop_display(request, vid_id, frame_num=0, finish=0):
    context={}
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
        context['template']=getTemplate(request)
        context['frame']=f
        context['form']=form
        return render(request, 'video_crop.html', context)

def profile(request):
    context={}
    context['template']=getTemplate(request)
    return render(request, 'profile.html', context)


def register(request):
    context={}
    
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username}'s account created.")
            return redirect('login')
        else:
<<<<<<< HEAD
            context["form"] = form
=======
            context['form']=form
>>>>>>> zl252
    else:
        form = UserCreationForm()
        context['form']=form
    return render(request, 'register.html', context)

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

@login_required
def toggleTheme(request, theme):
    User.objects.filter(id=request.user.id).update(theme=theme)
    context={}
    context['template']=getTemplate(request)
    return redirect(request.META['HTTP_REFERER'], context)


def exportToCSV(request, l_id=0):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Video','Frame','User','Label','Timestamp','Value', 'Difference'])

    if l_id == 0:
        for data in ExtractedData.objects.filter(user=request.user).all():
            datalist=(data.video.name, data.frame.frameNum, data.user.username, data.label.name, data.timeStamp, data.value, data.valueChange)
            writer.writerow(datalist)
    else:
        for data in ExtractedData.objects.filter(user=request.user, label_id=l_id).all():
            datalist=(data.video.name, data.frame.frameNum, data.user.username, data.label.name, data.timeStamp, data.value, data.valueChange)
            writer.writerow(datalist)

    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    return response
