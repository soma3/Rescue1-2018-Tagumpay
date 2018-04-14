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
camera.framerate = 30
camera.sensor_mode = 2 #full pov
camera.resolution = (656, 452)
rawCapture = PiRGBArray(camera, size=(656, 452))

evaczone = 0
threshold = 1.4
minheight = 50

def evaczonedetection(img):
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img, cv2.COLOR_BGR2GRAY)
    ret, bin = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY_INV)
    image, contours, h = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x2,y2,w,h = cv2.boundingRect(cnt)
        ratio = float(h)/float(w) #w/h if camera rotated
        if (ratio>threshold) and (h>minheight):
            evaczone=1
        ser.write(struct.pack('b',evaczone)
        cv2.rectangle(output, (x2,y2), (x2+w,y2+h), (255,0,0),2) #for debugging
        print "start" #for debugging
        print w #for debugging
        print h #for debugging
        print ratio #for debugging
    cv2.imshow("output", output) #for debugging
    cv2.imshow("bin", bin) #for debugging
    return evaczone
#time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr",  use_video_port=True):
    if ser.read()==1 and evaczone != 1:
#      evaczone=0
      img=np.asarray(frame.array)
      img = imutils.resize(img,300)
      img = imutils.rotate_bound(img,90)
    
      evaczonedetection(img)
    
      print evaczone #f
      if (evaczone): #f
          cv2.putText(output, "rectangle", (10,50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,255,0)) #f
      else: #f
          cv2.putText(output, "nothing", (10,50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,255,0)) #f
      cv2.imshow("output", output) #f
      cv2.imshow("bin", bin) #f
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
      break



#for frame in camera.capture_continuous(rawCapture, format="bgr",  use_video_port=True):
#    evaczone=0
#    img=np.asarray(frame.array)
#    img = imutils.resize(img,300)
#
##    rawCapture.truncate()
#    output = img.copy()
##    canny = img.copy()
#    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
##    canny = cv2.Canny(gray, 80, 80)
#    out = gray.copy()
#    blur = cv2.GaussianBlur(gray,(5,5),0)
#    ret, bin = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY_INV)
#    image, contours, h = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #if error try countours,h
##    circles = cv2.HoughCircles(bin, cv2.HOUGH_GRADIENT, 1.2, 50, param1=80, param2=80, minRadius=15)
#    for cnt in contours:
#        x2,y2,w,h = cv2.boundingRect(cnt)
#        ratio = float(h)/float(w) #w/h if camera rotated
#        print ratio
#        if (ratio>threshold) and (h>minheight):
#            evaczone=1
###            if circles is not None:
###                circles = np.round(circles[0, :]).astype("int")
###                for (x,y,r) in circles:
###                    cv2.circle(output, (x, y), r, (0, 255, 0), 4)
###                    cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
###                    print "start"
###                    print x
###                    print y
###                    print r
###                    if ((x<x2)or(x>x2+w)) and ((y<y2)or(y>y2+h)):
###                        evaczone=1
###            else:
###                evaczone=1
#        cv2.rectangle(output, (x2,y2), (x2+w,y2+h), (255,0,0),2)
#        print "start"
#        print w
#        print h
#        print evaczone
#        if (evaczone):
#            cv2.putText(output, "rectangle", (10,50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,255,0))
#        else:
#            cv2.putText(output, "nothing", (10,50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,255,0))
#    cv2.imshow("output", output)
#    cv2.imshow("bin", bin)
##   cv2.imshow("canny", canny)
#    key = cv2.waitKey(1) & 0xFF
#    rawCapture.truncate(0)
#
#    if key == ord("q"):
#        break
#    #rawCapture.seek(0)
#    #if process(rawCapture):
#    #    break
#    # show the output image


cv2.waitKey(0)
cv2.destroyAllWindows()
