import robot
import time

R = robot.Robot()


left = R.motors[0]
right = R.motors[1]

def forwards(delay,comment,power):
	print comment
	R.motors[0].speed = power
	R.motors[1].speed = power
	time.sleep(delay)
	R.motors[0].speed = 0
	R.motors[1].speed = 0
	
def left(delay,comment,power):
	print comment
	R.motors[0].speed = -power
	R.motors[1].speed = power
	time.sleep(delay)
	R.motors[0].speed = 0
	R.motors[1].speed = 0
	
def right(delay,comment,power):
	print comment
	R.motors[0].speed = power
	R.motors[1].speed = -power
	time.sleep(delay)
	R.motors[0].speed = 0
	R.motors[1].speed = 0


def distance_orderer(listname):
    listname=sorted(listname, key=lambda Marker:Marker.distance)
    return listname
	


while True:
	
	
	markers = R.see((1280,1024),True,1)
	markers = distance_orderer(markers)	
	
	if len(markers)>0:
		print markers[0].distance
		primary = markers[0]
		if markers[0].bearing.y < -10:
			print "marker on the left"
			left(0.1,"turning left",100)
		elif markers[0].bearing.y > 10:
			right(0.1,"turning right",100)
			print "marker on the right"
			
		else:
			forwards(2,"going forwards",100)
	else:
		print "cant see any markers"
		left(0.3,"turning to look for markers",70)
	
	
	
