#modified from http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import serial
import time
import cv2

# frame variables
xFrame = 320
yFrame = 240
 

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (xFrame, yFrame)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(xFrame, yFrame))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	img = frame.array
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)
	minLineLength = 1
	maxLineGap = 10
	lines = cv2.HoughLinesP(edges,1,np.pi/180,20,minLineLength,maxLineGap)
	if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
                #cv2.imwrite('houghlines5.jpg',img)

	# show the frame
	cv2.imshow("Frame", img)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
        #if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break