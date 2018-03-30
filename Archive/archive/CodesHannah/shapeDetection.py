# import the necessary packages
import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import serial
import time

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

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied tetx
	image = frame.array
	# blur frame and convert it to the HSV
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	# find contours in the thresholded image and initialize the
	# shape detector
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	# loop over the contours
	for c in cnts:
			# compute the center of the contour, then detect the name of the
			# shape using only the contour
			M = cv2.moments(c)
			if M["m00"] >0:
                            cX = int((M["m10"] / M["m00"]) )
                            cY = int((M["m01"] / M["m00"]) )
                            c = c.astype("float")
                            c = c.astype("int")
                            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                            print cX
                            print cY
        # show the output image
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
			break


