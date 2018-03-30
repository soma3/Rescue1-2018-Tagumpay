# things that need to get done
# line track 
# - gaps at least 5cm of straight line before gap, gap no more than 20cm 
# - lines will be 10cm away from any edge of the arena 
# - straight line, zigzag, curves, gaps, circle and turning, 90 degree turns
# - speed bumps white in color
# - slope
# - obstacle
# - green 25mmx25mm 
# - if two green turn around
# - if no green go straight
# - there may be more than one green square on the intersections but not on the correct side
# - silver strip line track end

# collection 
# - movement for collection
# - ball detection
# - rescue zone detection
# - depositing
# - turning out of corners
# - timer limit 
# - robots may face obstacles and debris in the rescue zone
 
# so basically i need to be able to tell where the line is, x y cordinates of the middle
# i need to record this info if there previously is a black line before we get to a gap
# need to distinguish between 90 degree turns and intersections
# - probably will check the position of the horizontal line to see if it crosses the verticle line past the edge of the verticle line
# need a way to stop pid to do things like obstacle and gap and 90 degree turnings
# need a way to check green squares and the position of the green squares in relation to the x and y axis
# import the necessary packages
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
 
	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

img = cv2.imread('dave.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,200)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite('houghlines3.jpg',img)
