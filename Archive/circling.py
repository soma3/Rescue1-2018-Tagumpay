import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
camera.sensor_mode = 2
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640, 480))
 
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr",  use_video_port=True):
    img=np.asarray(frame.array)
#    rawCapture.truncate()
    output = img.copy()
#    canny = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 80, 80)
    blur = cv2.GaussianBlur(canny,(5,5),0)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.2, 50, param1=80, param2=80, minRadius=0)
    
# ensure at least some circles were found
    if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
    
    # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    cv2.imshow("output", output)
#    cv2.imshow("canny", canny) 
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