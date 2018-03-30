from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import imutils
import time
import serial
import struct


ser = serial.Serial(port='/dev/ttyACM0',baudrate=9600)
camera = PiCamera()
camera.framerate = 30 #what frame rate do we need 
camera.sensor_mode = 2 #full pov
camera.resolution = (656, 452)
rawCapture = PiRGBArray(camera, size=(656, 452))

def serPrint(r,l):
    if r > 100:
        r = 100
    if r < -100:
        r = -100
    if l > 100:
        l = 100
    if l< -100:
        l = -100
    l = int((l/100)*127)
    r = int((r/100)*127)
    print 'start'
    print r
    print l
    ser.write(struct.pack('bb', r, l))
    
def lineInfo (img, crop): #takes an image and returns where the centre of the line is, and how much line ...
    if crop: #crops the image if specified when the function was called
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
            x += M['m10']/M['m00'] #finds avarage x posn of the contour
            y += M['m01']/M['m00'] #finds average y posn of the contour
    if len(contour) != 0: 
        x = x/len(contour)
        y = y/len(contour)
        offset = width/2. - x
    return [offset, x, y, area, contour]
        
def greenPosn (hsv): # none = 0, right = 1, left = 2, both = 3
	lowergreen = np.array([65, 50, 50]) #threshold for what's green
	uppergreen = np.array([110, 255, 255])
	greenimg = cv2.inRange(hsv, lowergreen, uppergreen) #turns green to white and not green to black
	image,contour,heirarchy = cv2.findContours(greenimg, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE)
    	area = 0
	xgreen = 0
	ygreen = 0
	for x in contour:
            M = cv2.moments(x)
            area += M['m00']
            if M['m00'] != 0:
                xgreen += M['m10']/M['m00'] # am i supposed to average this?? idk
                ygreen += M['m01']/M['m00']
        if len(contour) != 0:
            xgreen = xgreen/len(contour)
            ygreen = ygreen/len(contour)
            #areaR = cv2.contourArea(contourR[0])
        if area < greenThresh:
            green = 0
        elif area > 2*greenThresh:
            green = 3
        else:
            height, width, channel= crop.shape
            cropdim = [int(ygreen+40),int(ygreen+80), 0,width]
            xline = (lineInfo(thresh,cropdim))[1] #+10 is to start below the start of the green and not the centre
            if xgreen > xline:
                green = 1
            else:
                green = 2
        return [green,xgreen, ygreen, area]

def invert(img):
    invertf = abs(255 - img)
    return invertf
        
def junc(img):
    img = invert(img)
    height, width = img.shape
    images = [img[0:height/3,width/3:2*width/3], img[height/3:2*height/3,0:width/3], img[height/3:2*height/3,2*width/3:width]]
    isblack = []
    for image in images:
        thing, contour, heirarchy = cv2.findContours(image, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE)
        area = 0
        for cnt in contour:
            area = area + cv2.contourArea(cnt)
        if area > blackThresh:
            isblack.append(1)
        else:
            isblack.append(0)
    if isblack[0] == 1:
        if isblack[1] == 1 or isblack[2] == 1:
            return[True]
        else:
            return[False]
    else:
        return[False]
integral = 0
preverror = 0

def linetrack(crop, lasterror, speed):
           
        offset = lineInfo(thresh,0)[0]
        kp = 0.8
        ki = 0
        kd = 1
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
    x = smallSlice
    while x <= height and lineInfo(invert(thresh),[height-x,height,0,width])[3] < islinethresh: 
        x += 1
    if x == height:
        lolol=7
        #motor move back
        ##serialprint something for it to move??             
    else:
        linetrack([height-smallSlice,height,0,width])

greenThresh = 2000
blackjuncThresh = 1000
islinethresh = 700
greenClose = 100
smallSlice = 50
offset = 0
motorleft = 0
motorright = 0
integral = 0
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
	'''if lineInfo(invert(thresh),[height-smallSlice,height,0,width])[3] > islinethresh:
            if greenPosn(hsv)[0]:
                lolol=6
                #greenline things
            elif junc(thresh[height-smallSlice,height,0,width]):
                lolol=6
                #gostraightpast it?? ok so now are we gonna
                #do junctionthing
            else:
                linetrack([height-smallSlice,height,0,width])
        else:
            dashLines()
        '''
        integral = 0
        preverror = linetrack([height-smallSlice,height,0,width],preverror,30)
    	rawCapture.truncate(0)
	cv2.imshow("Frame2", thresh)
	key = cv2.waitKey(10) & 0xFF
	
	if key == ord("q"):
                break