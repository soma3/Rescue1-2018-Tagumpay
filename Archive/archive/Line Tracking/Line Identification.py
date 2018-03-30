import numpy as np
import cv2

cv2.namedWindow("Frame")
# video capture from webcam
camera = cv2.VideoCapture(0)

while True:
	(grabbed, frame) = camera.read();

	# convert image to grayscale and smooth
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)

	# identify black segments
	ret,thresh = cv2.threshold(blur,80,255,cv2.THRESH_BINARY_INV)

	# find and draw out the edges of black segments
	img,contours,hierarchy = cv2.findContours(thresh.copy(),1,cv2.CHAIN_APPROX_NONE)	
	cv2.drawContours(frame, contours, -1, (0,255,0), 3)

	# display image
	cv2.imshow("Frame", frame)

	# wait until the 'q' key is pressed
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()