
from bdb import Breakpoint
from importlib.resources import path
from re import X
import sys

import numpy as np
import cv2

import os


image = cv2.imread(r'\515286401191\OppHealth\OppHealth_frame0.jpg')
img = image.copy()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,5)
#cv2.imshow('thresh', thresh)
#cv2.waitKey()
dim=img.shape
print(dim)
area=dim[0]*dim[1]


mask = np.zeros(image.shape, dtype=np.uint8)
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

samples =  np.empty((0,100))
responses = []
keys = [i for i in range(48,58)]

cv2.destroyAllWindows()
for cnt in contours:
    if cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<400:
        [x,y,w,h] = cv2.boundingRect(cnt)

        
        if h>18:
            x-=3
            y-=3
            w+=6
            h+=6
            print(w,h)
            #print(area)
            #print(approx)
            print(cv2.contourArea(cnt))
            cv2.drawContours(img,[cnt], 0, (36,255,12), 3)
            cv2.drawContours(mask,[cnt], 0, (255,255,255), -1)
            cv2.imshow('img', img)
            cv2.waitKey()
            cv2.destroyAllWindows
            cropped=img[y:y+h, x:x+w]
            cv2.imshow('crop',cropped)
            cv2.waitKey()
            cv2.destroyAllWindows

mask=cv2.bitwise_and(mask, img)

#cv2.imshow('mask', mask)
#cv2.waitKey()
