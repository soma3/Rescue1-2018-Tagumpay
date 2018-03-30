import numpy as np
import cv2
import os

# create a window named "Frame"
cv2.namedWindow("Frame")

# load a cat picture from opencv_lessons/Images
path = str(os.path.dirname(__file__)) + "/../Images/cat.jpeg"
image = cv2.imread(path, 1)

# resize the image to 1000 pixels wide and 650 pixels tall
image = cv2.resize(image, (1000,650))

# place the image in the window named "Frame"
cv2.imshow("Frame", image)

# wait until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()