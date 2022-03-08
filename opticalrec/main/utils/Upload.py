import cv2     # for capturing videos
import math   # for mathematical operations
import matplotlib.pyplot as plt    # for plotting the images
#get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
from keras.preprocessing import image   # for preprocessing the images
import numpy as np    # for mathematical operations
from keras.utils import np_utils
from pyparsing import And
from skimage.transform import resize   # for resizing images
from main.models import Frame
from main.models import ExtractedData
from main.models import videoResize
from opticalrec.settings import MEDIA_ROOT
import os


def videoIntoFrames(vid,label):
    videoFile=vid.videoFile.path
    user=vid.user
    count = 0
    crop=videoResize.objects.get(video_id=vid.id, label=label)
    user_folder = str(MEDIA_ROOT) + "/frames/" + str(user.username)
    video_folder = "/" + str(vid.id)
    if not os.path.isdir(user_folder):
        os.mkdir(user_folder)
    if not os.path.isdir(user_folder + video_folder):
        os.mkdir(user_folder+video_folder)
    if not os.path.isdir(user_folder + video_folder + '/' + crop.label):
        os.mkdir(user_folder+video_folder + '/' + crop.label)
    if Frame.objects.filter(video_id=vid.id).exists() and Frame.objects.filter(frameFile__contains='/frame0.jpg').exists():
        return "already exists"
    cap = cv2.VideoCapture(videoFile)   # capturing the video from the given path
    frameRate = cap.get(5) #frame rate
    x=1
    while(cap.isOpened()):
        frameId = cap.get(1) #current frame number
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate) == 0):
            cframe=frame[round(crop.y1*crop.nat_height):round(crop.y2*crop.nat_height), round(crop.x1*crop.nat_width):round(crop.x2*crop.nat_width)]
            filename ="frames/%s/%d/%s/%s_frame%d.jpg" % (user.username,vid.id, crop.label, crop.label, count)
            cv2.imwrite(str(MEDIA_ROOT) + "/" + filename, cframe)
            f=Frame()
            f.video=vid
            #f.user=user
            f.frameFile.name=filename
            f.frameNum=cap.get(cv2.CAP_PROP_POS_FRAMES)
            f.timeStamp=(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
            f.save()

            exd=ExtractedData()
            exd.video=vid
            exd.label=crop.label
            exd.user=user
            exd.value=count
            exd.valueChange=1
            exd.timeStamp=f.timeStamp
            exd.save()
            count+=1
    cap.release()
    return "Done!"



"""
img = plt.imread('clips_frames/clip1_frames/frame0.jpg')   # reading image using its name
plt.imshow(img)

data = pd.read_excel('mapping.xlsx')     # reading the csv file
data.head()      # printing first five rows of the file


X = [ ]     # creating an empty array
for img_name in data.Image_ID:
    img = plt.imread('clips_frames/clip1_frames/' + img_name)
    X.append(img)  # storing each image in array X
X = np.array(X)    # converting list to array


# In[13]:


print(X)


# In[14]:


y = data.Class
dummy_y = np_utils.to_categorical(y)    # one hot encoding Classes


# In[15]:


print(dummy_y)


# In[16]:


image = []
for i in range(0,X.shape[0]):
    a = resize(X[i], preserve_range=True, output_shape=(224,224)).astype(int)      # reshaping to 224*224*3
    image.append(a)
X = np.array(image)


# In[17]:


print(X)


# In[18]:


from keras.applications.vgg16 import preprocess_input
X = preprocess_input(X, data_format = None)      # preprocessing the input data


# In[19]:


from sklearn.model_selection import train_test_split
X_train, X_valid, y_train, y_valid = train_test_split(X, dummy_y, test_size=0.3, random_state=42)    # preparing the validation set


# In[20]:


from keras.models import Sequential
from keras.applications.vgg16 import VGG16
from keras.layers import Dense, InputLayer, Dropout


# In[23]:


import ssl
ssl._create_default_https_context = ssl._create_unverified_context

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3)) 


# In[24]:


X_train = base_model.predict(X_train)
X_valid = base_model.predict(X_valid)
X_train.shape, X_valid.shape


# In[25]:


X_train = X_train.reshape(28, 7*7*512)      # converting to 1-D
X_valid = X_valid.reshape(12, 7*7*512)


# In[26]:


train = X_train/X_train.max()      # centering the data
X_valid = X_valid/X_train.max()


# In[27]:


# i. Building the model
model = Sequential()
model.add(InputLayer((7*7*512,)))    # input layer
model.add(Dense(units=1024, activation='sigmoid')) # hidden layer
model.add(Dense(2, activation='softmax'))    # output layer


# In[28]:


model.summary()


# In[29]:


# ii. Compiling the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[30]:


# iii. Training the model
model.fit(train, y_train, epochs=100, validation_data=(X_valid, y_valid))


# In[110]:


count = 0
videoFile = "clips/clip1.mp4"
cap = cv2.VideoCapture(videoFile)
frameRate = cap.get(5) #frame rate
x=1
while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if (frameId % math.floor(frameRate) == 0):
        filename ="clips_frames/clip1_frames_analyzed/test%d.jpg" % count;count+=1
        cv2.imwrite(filename, frame)
cap.release()
print ("Done!")


# In[31]:


test = pd.read_excel('test.xlsx')


# In[32]:


test_image = []
for img_name in test.Image_ID:
    img = plt.imread('clips_frames/clip1_frames_analyzed/' + img_name)
    test_image.append(img)
test_img = np.array(test_image)


# In[33]:


test_image = []
for i in range(0,test_img.shape[0]):
    a = resize(test_img[i], preserve_range=True, output_shape=(224,224)).astype(int)
    test_image.append(a)
test_image = np.array(test_image)


# In[34]:


# preprocessing the images
test_image = preprocess_input(test_image, data_format = None)

# extracting features from the images using pretrained model
test_image = base_model.predict(test_image)

# converting the images to 1-D form
test_image = test_image.reshape(40, 7*7*512)

# zero centered images
test_image = test_image/test_image.max()


# In[36]:


predict_x=model.predict(test_image) 
classes_x=np.argmax(predict_x,axis=1)


# In[43]:


print("The screen time of HEALTH is", classes_x[classes_x==1].shape[0], "seconds")
print("The screen time of NO HEALTH is", classes_x[classes_x==0].shape[0], "seconds")


"""
