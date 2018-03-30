# importing things

from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import imutils # for things like resizing (?)
import time


# CHANGE CAMERA MODE SOMEWHERE?
camera = PiCamera()
camera.framerate = 32
camera.sensor_mode = 2
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
 
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
	blur = cv2.GaussianBlur(gray,(5,5),0) # remove noise
	
	# crop = frame [ ... ] # crop to the part you need

	# identify black segments (img, maxval, ..., constant to add on. )
	ret = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, -3) 
	
##	canny edge detection (to give an image of a line?)
	can = cv2.Canny(blur, 70, 10, 17)
	cv2.imshow("Frame", blur)
	key = cv2.waitKey(1) & 0xFF
	
	# find equations of lines (p2 + p3 : resolution, p4: threshold, p5: min length for line, p6: how far spaced can lines be
	lines = cv2.HoughLinesP(can, 5, 0.05, 100, 0, 10)
	# linesn = cv2.HoughLines(can, 5, 0.05, 100)
	
	# find out which two vectors are the bottom most ones?
	#print(lines)
	#print(linesn)
	
	
	
camera.release()
cv2.destroyAllWindows()

















''' 
Canny Edge Detection (can use in place of / after threshold too): 
	- Finds the gradient (of pixel intensity). 
	- if above a certain treshold, it is an edge. 
	- if it is below another threshold, it isn't. 
	- if it's between the 2 thresholds, its a line if its next to an accepted line
	- Returns an image with just the edges
	
Find Contours: 
	- detects contours
	- how are contours defined act?
		- every single coordinate of the contour
		- would have to somehow find where the line is (moments ? to find cg for example)
	- could technically use this by splitting the thing into 9 or something to find the cg in ech individual one. 
	
Hough Line Transform: 
	- detects straight lines
	- rho and theta affect the precision of the detected line (tradeoff with time taken i guess)
	- how the transform actually works:
		- every line can be represented by a point in the Hough Space (HS)
		- so a line/curve in a HS is drawn for the set of lines that pass through each point in the image. 
		- the point where most of these lines in HS intersect represents the best fit line (for the image)
		- an accumulator (???) is used to find out this intersection 
			- (the resolution of the accumulator affects the precision of the detected line)		
	- is treshold a percentage???
		
		
Hough Line Transform Prob.:
	- binary image --> many output vector lines
	- others pretty much the same?
	- min for range of line segments you want
	- and max for the gap between points

'''