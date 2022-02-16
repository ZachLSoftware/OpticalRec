import cv2
import os
from main.models import Frame
from opticalrec.settings import MEDIA_ROOT
from main.models import Video

def preview_frame(vid):
    if Frame.objects.filter(video_id=vid.id).filter(frameFile__contains="previewFrame"):
        return Frame.objects.filter(video_id=vid.id).get(frameFile__contains="previewFrame")
    # Opens the inbuilt camera of laptop to capture video.
    cap = cv2.VideoCapture(vid.videoFile.path)

    ret, frame = cap.read()
        
    filename ="frames/%d/previewFrame.jpg" % (vid.id)
    if not os.path.isdir(str(MEDIA_ROOT) + "/frames/" + str(vid.id)):
        os.mkdir(str(MEDIA_ROOT) + "/frames/" + str(vid.id))
    cv2.imwrite(str(MEDIA_ROOT) + "/" + filename, frame)
    f=Frame()
    f.video=vid
    f.userId=0
    f.frameFile.name=filename
    f.frameNum=1
    f.save()

    cap.release()
    cv2.destroyAllWindows()
    return f