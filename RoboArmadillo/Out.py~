import serial
import time
import sys,os

ser = serial.Serial("/dev/ttyACM0",9600, timeout= 2)

#apparently you can't int() 0 soooo for the purposes of
#serialing then 1 = False and 2 = True


class Output(object):
    def __init__(self, which_pin, d = False):
        self._d = d
        self._pin_no = which_pin
	self._dispatch_val = 0
	global ser


    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, d):
        self._d = d
	if self._d == False:
		self._dispatch_val = 1
	elif self._d == True:
		self._dispatch_val =2
	else:
		print "CODE EXITED with ERROR 6: Digital Output Pins needs Boolean[True/False] input"
		sys.exit()

	if self._d == True or self._d == False:
		print "sending data"
		ser.write("4" +"," + str(self._pin_no)+"," +str(self._dispatch_val))
		a =ser.readline()
		time.sleep(0.5)
		print a
            	if not int(a) == int(self._dispatch_val):
                	print "CODE EXITED with ERROR 1: Serial Error"
                	sys.exit()
	

        
	
    @d.deleter
    def d(self):
        del self._d
