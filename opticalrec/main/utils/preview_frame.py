import cv2
import os
from main.models import Frame
from opticalrec.settings import MEDIA_ROOT
from main.models import Video

def preview_frame(vid,fnum):
    user_folder = str(MEDIA_ROOT) + "/frames/" + vid.user.username
    video_folder = "/" + str(vid.id)

    if not os.path.isdir(user_folder):
        os.mkdir(user_folder)
    if not os.path.isdir(user_folder + video_folder):
        os.mkdir(user_folder + video_folder)
    if Frame.objects.filter(video_id=vid.id).filter(frameFile__contains="previewFrame"):
        return Frame.objects.filter(video_id=vid.id).get(frameFile__contains="previewFrame")
    # Opens the inbuilt camera of laptop to capture video.
    cap = cv2.VideoCapture(vid.videoFile.path)
    if fnum>cap.get(cv2.CAP_PROP_FRAME_COUNT):
        fnum = 0
    cap.set(1, fnum)
    ret, frame = cap.read()
        
    filename ="frames/%s/%d/previewFrame.jpg" % (vid.user.username, vid.id)

    cv2.imwrite(str(MEDIA_ROOT) + "/" + filename, frame)
    f=Frame()
    f.video=vid
    f.user=vid.user
    f.frameFile.name=filename
    f.timeStamp=(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
    f.frameNum=int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    f.save()

    cap.release()
    cv2.destroyAllWindows()
    return f