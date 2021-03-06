import servo
import motor
import Out
import In
import time
import serial
import random
import os,sys
from pykoki import *
from cv2 import *
import Staff_In
import picamera
from vision import *

'''
Created By Adam Ferguson (RoboPython @ RoboArmadillo) 2013
'''




'''
###BOARD CODES###
1-Servos
2-Motors
3-Output - Digital
4-Input - Analog
5-Input - Digital
#################
'''

ser = serial.Serial("/dev/ttyACM0",115200, timeout= 2)
round_length = 180

class Robot(object):
	def __init__(self):
		self.zone = 0
		self.mode = "dev"
		global ser
		self.servos = [ servo.Servo(0,0),
				servo.Servo(1,0),
				servo.Servo(2,0),
				servo.Servo(3,0),
				servo.Servo(4,0),
				servo.Servo(5,0),
				servo.Servo(6,0),
				servo.Servo(7,0)]


		self.motors = [	motor.Motor(0,0),
				motor.Motor(1,0),
				motor.Motor(2,0),
				motor.Motor(3,0)]


		self.outputs = [Out.Output(0,0),
				Out.Output(1,0),
				Out.Output(2,0),
				Out.Output(3,0),
				Out.Output(4,0),
				Out.Output(5,0),
				Out.Output(6,0),
				Out.Output(7,0),]


		self.inputs = [ In.Input(0,0),
				In.Input(1,0),
				In.Input(2,0),
				In.Input(3,0),
				In.Input(4,0),
				In.Input(5,0),
				In.Input(6,0),
				In.Input(7,0),
				In.Input(8,0),
				In.Input(9,0),
				In.Input(10,0),
				In.Input(11,0),
				In.Input(12,0),
				In.Input(13,0),
				In.Input(14,0),
				In.Input(15,0)]
		
		self.staff_inputs = [ Staff_In.Input(0,0),
				Staff_In.Input(1,0),
				Staff_In.Input(2,0)]


		self.a = ser.readline().rstrip()
		while str(self.a) == "":
			self.a = ser.readline().rstrip()
		print "SWITCHES ON"

		'''
		while True:
			a = self.staff_inputs[0].d
			b = self.staff_inputs[1].d
			c = self.staff_inputs[2].d
			if a == True:
				if self.zone <= 2:
					self.zone +=1
				elif self.zone == 3:
					self.zone = 0
				print "Your zone is:" + str(self.zone)
			
			if b == True:
				if self.mode == "dev":
					self.mode = "comp"
				elif self.mode == "comp":
					self.mode = "dev"
				print "Your mode is:" + self.mode
			
			if c == True:
				print "Starting User Code..."
				break
		'''
		def Timer_exit(round_length):
			while True:
				time.sleep(round_length)
				print "END OF ROUND, NOW EXITING CODE."
				thread.interrupt_main()

		if self.mode == "comp":
			thread.start_new_thread(Timer_exit,(round_length))


	def see(self, (WIDTH, HEIGHT)=(1280,1024), preview=True, preview_time=1):
            n=vision_see((WIDTH, HEIGHT), preview, preview_time)
            return n 
