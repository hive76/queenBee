"""
ArduinoProbe.py - Kyle Yankanich
This script is designed to monitor an arduino running Firmata
for a button press, and update beaconFile with the 
current timestamp when it is pressed

"""

import time, web
from firmata import *

beaconDelay = 3600
global beaconFile
beaconFile = '/home/irssi/beacon'
global beaconURL
beaconURL = r'http://beacon.hive76.org/index.php?status='
global prevTime
prevTime = time.time()


a = Arduino('/dev/ttyUSB0')
a.pin_mode(10, firmata.INPUT)

while True:
	a.parse()
	#print a.digital_read(10)
	timeDiff = (time.time() - prevTime)
	if (a.digital_read(10) == 1 and timeDiff > 1):
		print a.digital_read(10)
		print "BUTTON 10 PRESSED"
		print "ACTIVATE DA BEACON"
		print "timeDiff: " + str( timeDiff )
		f = open(beaconFile, 'w')
		f.write(str(int(time.time())))		
		f.close()
		web.get(beaconURL + "ACTIVE")
		#phenny.msg('#hive76bots', "Beacon has been activated")
		a.digital_write(9, firmata.HIGH)
		a.delay(0.5)
		prevTime = time.time()
