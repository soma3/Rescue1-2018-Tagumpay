import numpy as np
import cv2

cv2.namedWindow("Frame")
# video capture from webcam
camera = cv2.VideoCapture(0)

while True:
	# read from the camera: 
	# grabbed is a boolean value (True/False) of whether video was successfully captured
	# frame is the image still
	(grabbed, frame) = camera.read();

	# show the image still
	cv2.imshow("Frame", frame);

	# wait until the 'q' key is pressed
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

# do some cleanup
camera.release()
cv2.destroyAllWindows()