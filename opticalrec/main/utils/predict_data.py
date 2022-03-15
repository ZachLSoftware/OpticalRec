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


f=open(os.path.join(BASE_DIR,'main/utils/model_attr.json'))
model_attr=json.loads(f.read())
f.close()
class_names=model_attr['class_names']
model = tf.keras.models.load_model(os.path.join(BASE_DIR, (model_attr['model'])))
img_height=model_attr['img_height']
img_width=model_attr['img_width']
color=model_attr['color_mode']

def predict(img_path):
    
 
    img = tf.keras.utils.load_img(
    img_path, target_size=(img_height, img_width), color_mode=color
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



def eval_data(label):
    frames=Frame.objects.filter(label_id=label)
    prev=None
    for f in frames:

        current=predict(str(os.path.join(MEDIA_ROOT,str(f.frameFile))))
        if current != 'none' and current != 'covered' and current != 'done':
            if prev==None:
                prev=current
                exd=ExtractedData()
                exd.frame=f
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
                nextframe=Frame.objects.get(label_id=label, timeStamp=f.timeStamp+1)
                #twoframe=Frame.objects.get(label_id=label, timeStamp=f.timeStamp+2)
                next=predict(str(os.path.join(MEDIA_ROOT,str(nextframe.frameFile))))
                #two=predict(str(os.path.join(MEDIA_ROOT,str(twoframe.frameFile))))
                if next==current:
                    exd=ExtractedData()
                    exd.frame=f
                    exd.video=f.video
                    exd.label=f.label
                    exd.user=f.video.user
                    exd.value=current
                    exd.valueChange=int(current)-int(prev)
                    exd.timeStamp=f.timeStamp
                    exd.save()
                    prev=current
                else:
                    continue
