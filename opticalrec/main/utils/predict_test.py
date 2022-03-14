import numpy as np
import os
import PIL
import tensorflow as tf
import pathlib
from numpy import argmax
import cv2

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

def predict(img_path):
    class_names=['0', '1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '3', '30', '31', '4', '5', '6', '7', '8', '9', 'covered', 'done', 'none'] 
    new_model = tf.keras.models.load_model(r'grayscale.h5')
    

    img_height = 180
    img_width = 180
 
    
    img = tf.keras.utils.load_img(
    img_path, target_size=(img_height, img_width), color_mode="grayscale"
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    
    prediction = new_model.predict(img_array)
    score = tf.nn.softmax(prediction[0])
    classes=prediction.argmax(axis=-1)
    print(class_names[np.argmax(prediction)])
    print(prediction.argmax(axis=-1))

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )
    cv2.imshow('img', cv2.imread(img_path, cv2.IMREAD_GRAYSCALE))
    cv2.waitKey()
    cv2.destroyAllWindows()

from os import listdir
from os.path import isfile, join

mypath = r'C:\Users\zacha\OneDrive - University of Leicester\Year 2\CO2201\Group_10\Training\test'
save = r'C:\Users\zacha\OneDrive - University of Leicester\Year 2\CO2201\Group_10\Training'
used = r'C:\Users\zacha\OneDrive - University of Leicester\Year 2\CO2201\Group_10\Training\used/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for f in onlyfiles:
    predict(mypath+ '/' + f)