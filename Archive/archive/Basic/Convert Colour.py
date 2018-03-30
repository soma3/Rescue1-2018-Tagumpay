import numpy as np
import cv2
import os

# create 3 windows 
cv2.namedWindow("Gray")
cv2.namedWindow("HSV")

# load and resize the image
path = str(os.path.dirname(__file__)) + "/../Images/rgb.jpg"
image = cv2.imread(path, 1)
image = cv2.resize(image, (1000,650))

# convert image to grayscale
image_gray = image #cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
b,g,r = cv2.split(image)

# display both images
cv2.imshow("HSV", g)
cv2.imshow("Gray", image_gray)

# wait until key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()