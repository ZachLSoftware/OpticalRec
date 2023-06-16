from bdb import Breakpoint
from importlib.resources import path
from re import X


def get_contours(filename, save_path, used_path, f, d):
    import sys

    import numpy as np
    import cv2
    import easygui
    import os
    save_path = save_path +'\\data\\'
    im = cv2.imread(filename)
    im3 = im.copy()

    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,-30)
    #ret, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)


    #################      Now finding Contours         ###################

    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    samples =  np.empty((0,100))
    responses = []
    keys = [i for i in range(48,58)]
    cv2.imshow('im', im)
    #num=easygui.enterbox('What is the number?')
    num=d
    if not os.path.isdir(save_path + str(num)):
        os.mkdir(save_path + str(num))
    cv2.imwrite(save_path + str(num) +'/' + f[:-4] + '_ori.jpg', im)
    #cv2.imwrite(save_path + str(num) +'/'+f[:-4] + '_contrast.jpg', thresh)
    #cv2.imwrite(save_path + str(num) +'/'+f[:-4] + '_invert.jpg', 255-thresh)
    count=0
    
    cv2.destroyAllWindows()
    for cnt in contours:
        if cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<400:
            [x,y,w,h] = cv2.boundingRect(cnt)
            y-=2
            x-=2
            h+=4
            w+=4
            #print(cnt)
            #print(x,y, w,h)
            #print(cv2.contourArea(cnt))
            if h>18:# and h<30 and w>8 and w<23:
                #cv2.drawContours(im, cnt,0,255,-1)
                crop_img = im[y:y+h, x:x+w]
                cv2.imshow('crop', crop_img)
                num=easygui.enterbox('What is the number?')
                while num=='x':
                    y-=2
                    x-=2
                    h+=4
                    w+=4                    
                    crop_img = im[y:y+h, x:x+w]
                    cv2.imshow('crop', crop_img)
                    num=easygui.enterbox('What is the number?')
                if not os.path.isdir(save_path +str(num)):
                    os.mkdir(save_path + '/' + str(num))
                cv2.imwrite(save_path + str(num) +'/'+f[:-4] +'_cropped' + str(count) + '.jpg', crop_img)
                
                crop_img = thresh[y:y+h, x:x+w]
                #cv2.imwrite(save_path + str(num) +'/'+f[:-4] +'_cropped_contrast' + str(count) + '.jpg', crop_img)
                crop_img=(255-crop_img)
                #cv2.imshow("cropped", crop_img)
                #cv2.imwrite(save_path + str(num) +'/'+f[:-4] +'_cropped_invert' + str(count) + '.jpg', crop_img)
                count+=1
                #cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                
                cv2.destroyAllWindows()
    #os.rename(filename, used_path+f)
                
from os import listdir
from os.path import isfile, join, isdir
mypath = r'Group_Project\group-10\opticalrec\media\frames\393912236526\Health'
save = r'\CO2201\Group_10\training\test'
used = r'\CO2201\Group_10\training\test\used/'
onlydir = [f for f in listdir(mypath) if isdir(join(mypath, f))]



onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles.sort(key=len)
if onlyfiles:
    for f in onlyfiles:
        get_contours(join(mypath, f), save, used, f, 'double')

        
