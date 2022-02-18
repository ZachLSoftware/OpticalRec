import cv2
import os
from main.models import Frame
from opticalrec.settings import MEDIA_ROOT
from main.models import Video

def preview_frame(vid):
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

    ret, frame = cap.read()
        
    filename ="frames/%s/%d/previewFrame.jpg" % (vid.user.username, vid.id)

    cv2.imwrite(str(MEDIA_ROOT) + "/" + filename, frame)
    f=Frame()
    f.video=vid
    f.user=vid.user
    f.frameFile.name=filename
    f.frameNum=1
    f.save()

    cap.release()
    cv2.destroyAllWindows()
    return f