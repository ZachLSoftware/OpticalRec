import numpy as np
import os
import tensorflow as tf
from numpy import argmax
import cv2
from main.models import Frame, ExtractedData
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from opticalrec.settings import MEDIA_ROOT, BASE_DIR
import json


f=open(os.path.join(BASE_DIR,'main/utils/class_names.dat'), 'r')
class_names=json.loads(f.read())
f.close()
print(class_names)
model = tf.keras.models.load_model(os.path.join(BASE_DIR,'main/utils/grayscale.h5'))


def predict(img_path):
    
    img_height = 180
    img_width = 180
 
    img = tf.keras.utils.load_img(
    img_path, target_size=(img_height, img_width), color_mode="grayscale"
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    
    prediction = model.predict(img_array)
    score = tf.nn.softmax(prediction[0])
   
    return class_names[np.argmax(prediction)]

    """
    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )
    cv2.imshow('img', cv2.imread(img_path, cv2.IMREAD_GRAYSCALE))
    cv2.waitKey()
    cv2.destroyAllWindows()"""


def get_contour(img_path):
    image = cv2.imread(img_path)
    img = image.copy()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,5)

    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    #samples =  np.empty((0,100))
    results = []
    #keys = [i for i in range(48,58)]
    count=0
    for cnt in contours:
        if cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<400:
            [x,y,w,h] = cv2.boundingRect(cnt)

            if h>18:
                if x>3 and y > 3:
                    x-=3
                    y-=3
                    w+=6
                    h+=6
                cropped=img[y:y+h, x:x+w]
                p=os.path.join(MEDIA_ROOT,'cnt/'+str(count)+'.jpg')
                cv2.imwrite(p,cropped)
                results.append((x,p))
                count+=1
    results.sort()
    return results

def eval_data(label):
    frames=Frame.objects.filter(label_id=label)
    prev=None
    for f in frames:
        split=get_contour(str(os.path.join(MEDIA_ROOT,str(f.frameFile))))
        if split:
            num=''
            for s in split:
                new=(predict(s[1]))
                if new!='none' and new != 'covered' and new != 'done':
                    num=num+new

        current=predict(str(os.path.join(MEDIA_ROOT,str(f.frameFile))))
        if current != 'none' and current != 'covered' and current != 'done':
            if prev==None:
                prev=current
                exd=ExtractedData()
                exd.video=f.video
                exd.label=f.label
                exd.user=f.video.user
                exd.value=current
                exd.valueChange=0
                exd.timeStamp=f.timeStamp
                exd.save()
            elif prev==current:
                continue
            else:
                exd=ExtractedData()
                exd.video=f.video
                exd.label=f.label
                exd.user=f.video.user
                exd.value=current
                exd.valueChange=int(prev)-int(current)
                exd.timeStamp=f.timeStamp
                exd.save()
                prev=current
