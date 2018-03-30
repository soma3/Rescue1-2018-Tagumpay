# modified from https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
# import the necessary packages
from collections import deque
import numpy as np
import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import serial
import time

# frame variables
xFrame = 640
yFrame = 480
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (xFrame, yFrame)
camera.framerate = 32
camera.sensor_mode = 2
camera.rotation = 270
rawCapture = PiRGBArray(camera, size=(xFrame, yFrame))
 
# allow the camera to warmup
time.sleep(0.1)

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	
	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
#camera.release()
#cv2.destroyAllWindows()