import os,sys
import serial
import time
from pykoki import *
from cv2 import *
import picamera

camera = picamera.PiCamera()

def width_from_code(code):

    if code <= 100:
        code -= 100

    if code <= 27:
        return 0.25 * (10.0/12.0) #0.25 is printed width, inc. white border

    return (0.1 * (10.0/12.0))/2 #bodge fix as I literally have no idea what these numbers are

def vision_see((WIDTH, HEIGHT), preview, preview_time):

		params = CameraParams(Point2Df(WIDTH/2, HEIGHT/2),
                	      		Point2Df(WIDTH, HEIGHT),
                      			Point2Di(WIDTH, HEIGHT))
		
                camera.resolution = (WIDTH, HEIGHT)
                camera.vflip=False
                if preview:
                        camera.start_preview()
                        time.sleep(preview_time)
                        camera.stop_preview()
                camera.capture("lastpic.jpg")                            
		pic=cv2.cv.LoadImage("lastpic.jpg",CV_LOAD_IMAGE_GRAYSCALE) 
		k = PyKoki()
		m = k.find_markers_fp(pic, width_from_code, params) #from basic_example.py
		return m
