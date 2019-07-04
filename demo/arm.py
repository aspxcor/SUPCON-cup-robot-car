import serial
from FractalMind import *
import cv2
import time

ser = serial.Serial("/dev/serial0", 9600)

def servo(n, angle, speed):
    ser.write(GetMessage(n, angle, speed))
    
i = 6
while True:
    
    ser.write(GetMessage(3, 90, 40))
    ser.write(GetMessage(2, 100, 40))
    ser.write(GetMessage(1, 60, 40))
    ser.write(GetMessage(4, 140, 40))
    time.sleep(0.3)
    ser.write(GetMessage(i, 40, 40))
    time.sleep(10)
    ser.write(GetMessage(i, 70, 40))
    time.sleep(0.5)
