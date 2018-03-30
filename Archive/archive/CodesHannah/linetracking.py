import numpy as np

import cv2

import Adafruit_BBIO.GPIO as GPIO #probably dont need this

import imutils

import serial

import time


video_capture = cv2.VideoCapture(-1)

video_capture.set(3, 160)

video_capture.set(4, 120)

 

# Setup serial port

ser = serial.Serial(
              
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )
def GreenSquare():
   # attempt to read the green square, currently it doesnt actually tell the motors anything cause i need to find a way to stop PID and do the turning
    greenLower = (29, 86, 6) #need to find out what these values are 
    greenUpper = (64, 255, 255)
    RGB = cv2.cvtColor(crop_img,cv2.COLOR_BGR2RGB)
    Gmask = cv2.inRange(RGB, greenLower, greenUpper)
	Gmask = cv2.erode(Gmask, None, iterations=2)
	Gmask = cv2.dilate(Gmask, None, iterations=2)
    Gc = max(contours, key=cv2.contourArea)
    GM = cv2.moments(Gc)
    cx = int(GM['m10']/GM['m00']) #honestly i have no idea if this will screw up but basically im trying to find the coordinates of the green square
    cy = int(GM['m01']/GM['m00'])
    if cx <50:
        ser.write("Turn Left")
    if cx >120:
        ser.write("Turn Right")


while(True):

 

    # Capture the frames

    ret, frame = video_capture.read()

 

    # Crop the image

    crop_img = frame[60:120, 0:160]

 

    # Convert to grayscale

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

 

    # Gaussian blur

    blur = cv2.GaussianBlur(gray,(5,5),0)

 

    # Color thresholding

    ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

 

    # Erode and dilate to remove accidental line detections

    mask = cv2.erode(thresh1, None, iterations=2)

    mask = cv2.dilate(mask, None, iterations=2)

 

    # Find the contours of the frame

    contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

 

    # Find the biggest contour (if detected)

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        M = cv2.moments(c)

 

        cx = int(M['m10']/M['m00'])

        cy = int(M['m01']/M['m00'])

 

        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)

        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

 

        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

        print cx # can delete 

        print cy # can delete 

        ser.write(cx) # writes to the arduino to tell it its position relative to the x value this probably wouldnt work cause string might be necessary 

'''currently if the bot is too much to the right cx>120, 
       if too much to the left its cx<=50 and if its just right cx<120 and cx>50'''




    #Display the resulting frame

    cv2.imshow('frame',crop_img)

    #this needs to be changed to if it detects the silver strip or maybe for testing a green strip 
    #although technically if its connected to the com ctrl-c 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break