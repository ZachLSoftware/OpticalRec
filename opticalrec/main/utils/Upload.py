import cv2     # for capturing videos
import math
from main.models import Frame, Label, videoResize, ExtractedData

from opticalrec.settings import MEDIA_ROOT
import os


def videoIntoFrames(vid):
    videoFile=vid.videoFile.path
    user=vid.user
    count = 0
    crops=videoResize.objects.filter(video_id=vid.id)
    if not crops:
        return "No selected areas"
    user_folder = str(MEDIA_ROOT) + "/frames/" + str(user.username)
    video_folder = "/" + str(vid.id)
    newCrops = []
    labels = {}
    if not os.path.isdir(user_folder):
        os.mkdir(user_folder)
    if not os.path.isdir(user_folder + video_folder):
        os.mkdir(user_folder+video_folder)
    for crop in crops:
        labels[crop.label]=Label.objects.get(name=crop.label)
        if not os.path.isdir(user_folder + video_folder + '/' + crop.label):
            os.mkdir(user_folder+video_folder + '/' + crop.label)
        if Frame.objects.filter(video_id=vid.id, label=labels[crop.label]).filter(frameFile__contains='_frame').exists():
            continue
        else:
            newCrops.append(crop)
    if not newCrops:
        return "No New Crop Areas"


    cap = cv2.VideoCapture(videoFile)   # capturing the video from the given path
    frameRate = cap.get(5) #frame rate
    x=1
    while(cap.isOpened()):
        frameId = cap.get(1) #current frame number
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate) == 0):
            for crop in newCrops:
                cframe=frame[round(crop.y1*crop.nat_height):round(crop.y2*crop.nat_height), round(crop.x1*crop.nat_width):round(crop.x2*crop.nat_width)]
                flabel=Label.objects.get(video_id=vid.id, name=crop.label)
                filename ="frames/%s/%d/%s/%s_frame%d.jpg" % (user.username,vid.id, crop.label, crop.label, cap.get(cv2.CAP_PROP_POS_FRAMES))
                cframe=cv2.cvtColor(cframe, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(str(MEDIA_ROOT) + "/" + filename, cframe)
                f=Frame()
                f.video=vid
                f.label=labels[crop.label]
                #f.user=user
                f.frameFile.name=filename
                f.frameNum=cap.get(cv2.CAP_PROP_POS_FRAMES)
                f.timeStamp=(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
                f.save()

            
    cap.release()
    return "Done!"

