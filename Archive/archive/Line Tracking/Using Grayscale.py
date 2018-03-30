import numpy as np
import cv2

cv2.namedWindow("Frame")

def nothing(x):
	pass

# trackbar to play around with values
cv2.createTrackbar("Grayscale Threshold","Frame",0,255,nothing)

# video capture from webcam
camera = cv2.VideoCapture(0)

while True:
	(grabbed, frame) = camera.read();

	# convert image to grayscale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# a smoothing image function (gets rid of small image imperfections)
	blur = cv2.GaussianBlur(gray,(5,5),0)

	# threshold is a function to identify pixels in a certain range
	# all pixels above thresh_values become black, those below become white
	# thresh contains the modified image
	thresh_value = cv2.getTrackbarPos("Grayscale Threshold","Frame")
	ret,thresh = cv2.threshold(blur,thresh_value,255,cv2.THRESH_BINARY_INV)

	cv2.imshow("Frame", thresh)

	# wait until the 'q' key is pressed
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()