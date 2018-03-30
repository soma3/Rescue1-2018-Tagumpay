from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import imutils
import time
import serial

camera = PiCamera()
camera.framerate = 10
camera.sensor_mode = 2 #full pov
camera.resolution = (656, 452)
rawCapture = PiRGBArray(camera, size=(656, 452))
ser = serial.Serial(port='/dev/ttyACM2',baudrate=9600)

def xposn(lines):
	x = 0
	for line in lines:
		x = x + (line[0][0]+line[0][2])/2
	x = x/len(line)
	return x

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    resized = imutils.resize(image, 500)
    rotated = imutils.rotate_bound(resized,90)
    crop = resized[0:600,350:700]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY) # convert to grayscale
    blur = cv2.GaussianBlur(gray,(5,5),0) # remove noise
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize = 501, C = -10)
    canny = cv2.Canny(blur, 90, 70, apertureSize=3)
    line = cv2.HoughLinesP(canny, 1, 0.05, 15, minLineLength=30 , maxLineGap=20)
    if line is not None:
        avgx = xposn(line)
        print avgx
        error = 350./2. - avgx
        ser.write(bytes(errpr))

        i=0
        while i <len(line)-1: 
            cv2.line(blur,(int(line[i][0][0]),int(line[i][0][1])),(int(line[i][0][2]),int(line[i][0][3])),(0,255,0),2)
            i=i+1
    rawCapture.truncate(0)
    cv2.namedWindow("Frame")
    cv2.imshow("Frame",blur)
    
    key = cv2.waitKey(10) & 0xFF
	
    if key == ord("q"):
        break
    #ser.write(bytes(avgx))
    
    

    