# This module tests the performance of the camera
# and tries to get the key patterns of the 12 objects

import cv2 as cv

cap = cv.VideoCapture(1)

while cap.isOpened():
	_, frame = cap.read()

	cv.imshow('frame', frame)

	# filter out the environment

	# Rotate & Adjust

	# Calculate Width : Height

	if cv.waitKey(5) & 0xFF == ord('q'):
		break


cap.release()
cv.destroyAllWindows()
