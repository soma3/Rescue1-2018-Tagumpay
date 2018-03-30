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
evaczone = 0
threhold = 9
 
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr",  use_video_port=True):
    
    img=np.asarray(frame.array)
    img = imutils.resize(img,300)

#    rawCapture.truncate()
    output = img.copy()
#    canny = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    canny = cv2.Canny(gray, 80, 80)
    out = gray.copy()
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret, bin = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY_INV)
    image, contours, h = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #if error try countours,h
    
    # loop over the (x, y) coordinates and radius of the circles
    for cnt in contours:
        cnt_len = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt,0.1*cnt_len,True)
        if len(approx) < threhold and len(approx)>3:
            evaczone = 1
        cv2.drawContours(output,[cnt],-1,(255,0,0),2)
        if (evaczone):
            cv2.putText(output, "rectangle", (10,50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,255,0))
        else:
            cv2.putText(output, "nothing", (10,50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,255,0))
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
