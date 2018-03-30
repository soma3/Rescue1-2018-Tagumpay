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

	# find the edges of black segments
	img,contours,hierarchy = cv2.findContours(thresh.copy(),1,cv2.CHAIN_APPROX_NONE)	
	
	cv2.drawContours(frame, contours, -1, (0,255,0), 3)
	# if at least one black segment is found
	if len(contours)>0:
		# look at the biggest segment (probably the line) instead of smaller segments (probably noise)
		c = max(contours, key=cv2.contourArea)
		M = cv2.moments(c)

		# some math things to find the centroid (roughly the 'centre' of the segment)
		# for more information, google "moments image processing"
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		# draw the centroid into the frame
		cv2.circle(frame, (cx,cy), 3, (0,0,255),-1)

		'''
		if cx < width*0.5:
			line is on left, robot turns right
		else: 
			line is on right, robot turns left
		'''
	# display image
	cv2.imshow("Frame", frame)

	# wait until the 'q' key is pressed
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()