# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
camera.framerate = 30
camera.sensor_mode = 2 #full pov
camera.resolution = (656, 464)
rawCapture = PiRGBArray(camera, size=(656, 464))
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "grey"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (0,0,120)
greenUpper = (200,255,150)
pts = deque(maxlen=args["buffer"])
 
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	# resize the frame, blur it, and convert it to the HSV
	# color space
	rawCapture.truncate(0)
	image = frame.array
        frame = imutils.resize(image,300)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # show the frame to our screen
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
        img = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(img, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
	# update the points queue
	pts.appendleft(center)

	# loop over the set of tracked points
	for i in xrange(1, len(pts)):
		
		cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF
 
                # if the 'q' key is pressed, stop the loop
                if key == ord("q"):
                    break
 
	
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

