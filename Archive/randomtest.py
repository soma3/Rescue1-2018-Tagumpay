import numpy as np

'''a = [[1.456456456456,2.7687678876786,3.867867867867868,4.686788778786],[4.6867868,3.678676786,2.8989080,1.09789798678],[1.78789787897897897,1.6867678678678788,1.677677786868786,1.76876788767868786]]

for line in a:
    line = np.round(line, decimals=3, out=None)
    line = line.tolist()
    print line
   ''' 
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import imutils
import time

camera = PiCamera()
camera.framerate = 10
camera.sensor_mode = 2 #full pov
camera.resolution = (656, 452)
rawCapture = PiRGBArray(camera, size=(656, 452))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
        rawCapture.truncate(0)
	cv2.namedWindow("Frame")
        cv2.imshow('Frame',image)
        key = cv2.waitKey(10) & 0xFF
	
	if key == ord("q"):
                break