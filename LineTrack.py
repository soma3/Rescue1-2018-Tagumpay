#trying to push from raspi

from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import imutils
import time
import serial
import struct


ser = serial.Serial(port='/dev/ttyACM0',baudrate=9600) #change port to ACM1/2/3... if serial comm doesn't work
camera = PiCamera()
camera.framerate = 30 
camera.sensor_mode = 2 #full pov
camera.resolution = (656, 452)
rawCapture = PiRGBArray(camera, size=(656, 452))


    
def lineInfo (img, crop): #takes an image and returns where the centre of the line is, and how much line ...
    if crop: #crops the image if specified
        img = img[crop[0]:crop[1],crop[2]:crop[3]]
    image, contour, heirarchy = cv2.findContours(img, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE) #finds contours in the image
    area = 0
    x = 0
    y = 0
    height, width = img.shape #finds height and width of the image
    offset = 0
    for cnt in contour:
        M = cv2.moments(cnt)
        area += M['m00'] #finds total area of the black parts
        if M['m00'] != 0:
            x += M['m10']/M['m00'] #finds total x posn of the contour
            y += M['m01']/M['m00'] #finds total y posn of the contour
    if len(contour) != 0: 
        x = x/len(contour) #finds average x posn
        y = y/len(contour) #finds average y posn
        offset = width/2. - x
    return [offset, x, y, area, contour]
        
def greenPosn (hsv): #takes a hsv image and returns if there's green, where and how much green
	#none = 0, right = 1, left = 2, both = 3
	lowergreen = np.array([65, 50, 50]) #threshold for what's green
	uppergreen = np.array([110, 255, 255])
	greenimg = cv2.inRange(hsv, lowergreen, uppergreen) #turns green to white and not green to black
	image,contour,heirarchy = cv2.findContours(greenimg, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE) #finds contours
        area = 0
	xgreen = 0
	ygreen = 0
	for x in contour:
            M = cv2.moments(x)
            area += M['m00'] #finds total area
            if M['m00'] != 0:
                xgreen += M['m10']/M['m00'] 
                ygreen += M['m01']/M['m00'] 
        if len(contour) != 0:
            xgreen = xgreen/len(contour) # finds average x posn
            ygreen = ygreen/len(contour) # finds average y posn
        if area < greenThresh: #if there's very litte / no green
            green = 0 #there's no green square
        elif area > 2*greenThresh: #if there's alot of green
            green = 3 #it's a double green
        else:
            height, width, channel = crop.shape
            cropdim = [int(ygreen+40),int(ygreen+80), 0,width] #crops the image for 40 pixels below the green square
            xline = (lineInfo(thresh,cropdim))[1] #xposn of the line below the green square
            if xgreen > xline: #if green square lies on the right
                green = 1 #green square right
            else: 
                green = 2 #green square left
        return [green,xgreen, ygreen, area]

def invert(img): #takes an image and returns the negative of it (black -> white, white -> black)
    invertf = abs(255 - img)
    return invertf
        
def junc(img): #takes an image and detects if there is a t junction / intersection 
    img = invert(img) #takes negative of image
    height, width = img.shape
    images = [img[0:height/3,width/3:2*width/3], img[height/3:2*height/3,0:width/3], img[height/3:2*height/3,2*width/3:width]] #crops image to the top middle, middle left and middle right
    isblack = []
    for image in images: #for each crop 
        imag, contour, heirarchy = cv2.findContours(image, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE) #find the contours
        area = 0
        for cnt in contour:
            area = area + cv2.contourArea(cnt) #finds total area of black in crop 
        if area > blackThresh: #if there's enough black
            isblack.append(1) #there's a line
        else:
            isblack.append(0) #there isn't a line
    if isblack[0] == 1: #if top middle has a line
        if isblack[1] == 1 or isblack[2] == 1: #and either middle left or middle right has a line
            return[True] #there's a t junction / intersection
        else:
            return[False]
    else:
        return[False]

def serPrint(r,l): #takes a percentage of max power for each motor value, changes it range and serial prints it
	#if motor value more than max value, use max value
    if r > 100:
        r = 100
    if r < -100:
        r = -100
    if l > 100:
        l = 100
    if l < -100:
        l = -100
    l = int((l/100)*127) #scales values from -127 to 127
    r = int((r/100)*127)
    r = 80
    l = 80
    print 'start'
    print r
    print l
    ser.write(struct.pack('bb', r, l))

def linetrack(crop, lasterror, speed): #serial prints right and left motor values given image
           
        offset = lineInfo(thresh,0)[0] #finds offset of black line
        correction = 0
        inte = integral + offset 
        derivative = offset - lasterror
        correction = kp*offset + ki*inte + kd*derivative
        right = speed + correction
        left = speed - correction
        lasterror = offset
        serPrint(right,left)
        return lasterror
        
        
def dashLines():
    x = smallSlice #start with x being the height of the image we consider for normal linetrack
    while x <= height and lineInfo(invert(thresh),[height-x,height,0,width])[3] < isLineThresh: #if there is no line in the cropped img 
        x += 1 #increase x to check a larger part of the image for a line
        #break out if there isn't any line even if the whole image is considered 
    if x >= height: #if there wasn't any line even with the whole image
        lolol=7 #??? move back and straight until it sees line??
    else: #if there is a crop with enough black 
        lasterror = linetrack([height-x,height,0,width],lasterror,speed) #line track with that crop

def turn(time, dir): #turns right or left for a certain number of seconds if specified or else till a line is in the middle
#if dir = 1 turn right, if dir = -1 turn left
	if time > 0 : #if a time is specified
		t0 = time.time() #finds current time in timer
		while time.time() - t0 < time: #for the time specified
			serPrint(-dir*turnspeed, dir*turnspeed) #turn in the direction
	elif dir > 0: #if there isn't at time specified 
		while lineInfo(thresh, 0)[0] > 0: 
			serPrint(-dir*turnspeed, dir*turnspeed) #turn right until line is in the middle
	elif dir < 0: 
		while lineInfo(thresh,0)[0] < 0 :
			serPrint(-dir*turnspeed, dir*turnspeed) #turn left until the line is in the middle
			
def moveFwd(time,speed):
	t0 = time.time()
	while time.time - t0 < time:
		serPrint(speed,speed)

def overallFunc():
	green = greenPosn(hsv)[0]
	if green == 1:
		turn(2,1) #turn for a while to pass the line ahead
		turn(0,1) #turn till line is in the middle
	if green == 2:
		turn(2,-1) #turn for a while to pass the line ahead
		turn(0,-1) #turn till line is in the middle 
	if green == 3:
		turn(4,-1) #turn for a while to pass both lines
		turn(0,-1) #turn till the line is in the middle
	if green == 0:
		if junc(thresh) is True:
			moveFwd(1,30)
		if junc(thresh) is False:
			dashline()

greenThresh = 2000
blackjuncThresh = 1000
isLineThresh = 700
greenClose = 100
smallSlice = 50
offset = 0
speed = 30
motorleft = 0
motorright = 0
integral = 0
kp = 0.8
ki = 0
kd = 1
lasterror = 0 
turnspeed = 30
preverror = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
        resized = imutils.resize(image,300)
        rotated = imutils.rotate_bound(resized,90)
        height,width, channel = rotated.shape
        crop = rotated[height-smallSlice:height,0:width]
	hsv = cv2.cvtColor(crop, cv2.COLOR_RGB2HSV)
        hsv = hsv[height-smallSlice:height,0:width]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY) # convert to grayscale
        blur = cv2.GaussianBlur(gray,(5,5),0) # remove noise
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize = 501, C = 20)
	green = greenPosn(hsv)
        integral = 0
        preverror = linetrack([height-smallSlice,height,0,width],preverror,60)
        #overallFunc();
    	rawCapture.truncate(0)
	cv2.imshow("Frame2", thresh)
	key = cv2.waitKey(10) & 0xFF
	
	if key == ord("q"):
                break