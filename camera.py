## Camera

import cv2 as cv


class Camera:
	def __init__(self):
		self.cap = cv.VideoCapture(0)

