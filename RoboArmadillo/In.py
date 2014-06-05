import os,sys
import serial
import time 

ser = serial.Serial("/dev/ttyACM0",9600, timeout= 2)

#arduino won't read strings as im using getint() so changed query to 1

# you can't do int(0) so as always 1 is False, 2 is True

class Input(object):
    def __init__(self, which_pin, a = 6, d = False):
	global ser
        self._a = a
        self._d = d
        self._pin_no = which_pin
	self._ainput_value = 0
	self._dinput_value = False
        

    @property
    def a(self):
	print "sending data"
        ser.write("5" + "," +str(self._pin_no) +","+"1")
	check = ser.readline().rstrip()
	if str(check) == "1":
	     	self._ainput_value = ser.readline().rstrip()
		if self._ainput_value == "0" or "":
			self._a = 0
			return self._a
		else:
			self._a = float(self._a)
			self._a = self._ainput_value
			self._a = int(self._a) * 0.0049
			self._ainput_value = 0
			return float(self._a)
	else:
		print "CODE EXITED with ERROR 1: Serial Error"
    @a.setter
    def a(self, a):
        print "CODE EXITED with ERROR 5: You are not allowed to set input values"
        sys.exit()

    @a.deleter
    def a(self):
        del self._a


    @property
    def d(self):
        print "sending data"
        ser.write("6" + "," +str(self._pin_no) +","+"1")
	self._dinput_value = ser.readline().rstrip()
	print self._dinput_value
	self._dinput_value = ser.readline().rstrip()
	if str(self._dinput_value) =="1":
		self._d = False
		return self._d
	elif str(self._dinput_value) == "2":
		self._d =True
		return self._d
	
	else:
		print "CODE EXITED with ERROR ??: Arduino went funny, sorry"
		sys.exit()

       
    @d.setter
    def d(self, d):
        print "CODE EXITED with ERROR 5: You are not allowed to set input values"
        sys.exit()

    @d.deleter
    def d(self):
        del self._d
