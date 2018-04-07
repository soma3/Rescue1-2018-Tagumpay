import numpy as np
import cv2
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
camera.sensor_mode = 2
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640, 480))
evaczoneEntrance = 0
threshold = 1.4
minheight = 50
 
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr",  use_video_port=True):
    evaczoneEntrance=0
    img=np.asarray(frame.array)
    img = imutils.resize(img,300)

#    rawCapture.truncate()
    output = img.copy()
#    canny = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    canny = cv2.Canny(gray, 80, 80)
    out = gray.copy()
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret, bin = cv.adaptiveThreshold(img,127,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
    image, contours, h = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #if error try countours,h
    circles = cv2.HoughCircles(bin, cv2.HOUGH_GRADIENT, 1.2, 50, param1=80, param2=80, minRadius=15)
    for cnt in contours:
        x2,y2,w,h = cv2.boundingRect(cnt)
        ratio = float(h)/float(w) #w/h if camera rotated
        print ratio
        if (ratio>threshold) and (h>minheight):
            evaczoneEntrance=1
##            if circles is not None:
##                circles = np.round(circles[0, :]).astype("int")
##                for (x,y,r) in circles:
##                    cv2.circle(output, (x, y), r, (0, 255, 0), 4)
##                    cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
##                    print "start"
##                    print x
##                    print y
##                    print r
##                    if ((x<x2)or(x>x2+w)) and ((y<y2)or(y>y2+h)):
##                        evaczoneEntrance=1
##            else:
##                evaczoneEntrance=1
        cv2.rectangle(output, (x2,y2), (x2+w,y2+h), (255,0,0),2)
        print "start"
        print w
        print h
        print evaczoneEntrance
        if (evaczoneEntrance):
            cv2.putText(output, "Door", (10,50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,255,0))
        else:
            cv2.putText(output, "Nah", (10,50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,255,0))
    cv2.imshow("output", output)
    cv2.imshow("bin", bin)
#   cv2.imshow("canny", canny)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    
    if key == ord("q"):
        break
    #rawCapture.seek(0)
    #if process(rawCapture):
    #    break
    # show the output image
    

cv2.waitKey(0)
cv2.destroyAllWindows()
