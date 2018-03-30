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
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	r,b,g = cv2.split(image)
	
	# show the frame
	cv2.imshow("Frame", g)
        cv2.imshow("Frame1", b)

        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break