#!/usr/bin/env python
"""
beacon.py - Interfaces with the Hive76 beacon system 
beacon file = ~/beacon

This module was written by K. Yankanich, 
probably with help from dwfreed and peejay
"""
import time, threading, web, singleton
from firmata import *
import currentColor as c
from colors import LEDShift

global a
a = Arduino('/dev/ttyUSB0')
a.pin_mode(9, firmata.OUTPUT)
a.delay(2)

global beaconDelay
beaconDelay = 3600
global beaconFile
beaconFile = '/home/irssi/beacon'
global beaconURL
beaconURL = r'http://beacon.hive76.org/index.php?status='
global beaconStatus



def setup(phenny):
	def checkBeacon(phenny):
		global beaconStatus
		beaconStatus = True
		while not singleton.beaconPlzStop:
			"""check beacon """
			f = open(beaconFile)
			activated = int(f.read())
			f.close()
			if (int(activated) + beaconDelay) > int(time.time()):
				web.get(beaconURL + 'ACTIVE')
				a.digital_write(9, firmata.HIGH)
				LEDShift(a, c.currentColor, "00FF00", 2)
				time.sleep(2)
				LEDShift(a, "00FF00", c.currentColor, 2)
				if (beaconStatus == False):
					print "Beacon has been activated"
					phenny.msg('#hive76', "Beacon has been activated")
				beaconStatus = True
			else:
				web.get(beaconURL + 'INACTIVE')
				a.digital_write(9, firmata.LOW)
				LEDShift(a, c.currentColor, "FF0000", 2)
				time.sleep(2)
				LEDShift(a, "FF0000", c.currentColor, 2)

				if (beaconStatus == True):
					phenny.msg('#hive76', "Beacon has deactivated")
					print "Beacon has been deactivated"
				beaconStatus = False
			time.sleep(30)
	targs = (phenny,)
	if singleton.beaconThread is not None and singleton.beaconThread.isAlive():
		singleton.beaconPlzStop = True
		singleton.beaconThread.join()
		while singleton.beaconThread.isAlive():
			singleton.beaconThread.join()
		singleton.beaconPlzStop = False
	singleton.beaconThread = threading.Thread(target=checkBeacon, args=targs)
	singleton.beaconThread.start()


def beacon(phenny, input):
	global beaconURL, beaconStatus
	command = input.group(2)
	if command == 'on' and input.member:	
		f = open(beaconFile, 'w')
		f.write(str(int(time.time())))
		f.close()
                LEDShift(a, c.currentColor, "00FF00", 1)
                c.currentColor = "00FF00"
		a.digital_write(9, firmata.HIGH)

		web.get(beaconURL + "ACTIVE")
		phenny.say("Beacon has been activated")
		
	
		beaconStatus = True
		
	elif command == 'off' and input.member:
		f = open(beaconFile, 'w')
		f.write(str(int(time.time()) - beaconDelay))
		f.close()
	
		phenny.say("Beacon has been deactivated")
		a.digital_write(9, firmata.LOW)
		LEDShift(a, c.currentColor, "FF0000", 1)
		c.currentColor = "FF0000"
		web.get(beaconURL + "INACTIVE")
		beaconStatus = False		

	else:
		f = open(beaconFile)
		activated = int(f.read())
		f.close()
		if (int(activated) + beaconDelay) > int(time.time()):
			activeStr = time.ctime(int(activated))
			phenny.say("Beacon is active! Last activated at " + activeStr)
		else:
			phenny.say("Beacon is not activated")
			web.get(beaconURL + "INACTIVE")
			
beacon.commands = ['beacon']
beacon.priority = 'low'
