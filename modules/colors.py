"""
colors.py - Phenny RGB Arduino Firmata module

Kyle Yankanich
"""
import time, threading, sys, singleton
from subprocess import call
from firmata import *

sys.path.insert(0, '/home/irssi/phenny/modules/')
import currentColor as c


global a
a = Arduino('/dev/ttyUSB0')
a.pin_mode(3, firmata.PWM) #blue
a.pin_mode(5, firmata.PWM) #green
a.pin_mode(6, firmata.PWM) #red

def setup(phenny):
	def beaconHome(phenny):
		while True:
			b = open('/home/irrsi/phenny/beacon.info', "r")
			message = b.readlines()
			b.close()

			f = open('/home/irssi/phenny/beacon.info', "w")
			f.write(message[0])
			print message[0]
			f.write("\n")
			f.write(message[1])
			f.write("\n")
			f.write(message[2])
			f.write("\n")
			f.write(message[3])
			f.write("\n")
			f.write(c.currentColor)
			f.write("\n")
			f.close()

			time.sleep(10)

			call(["scp", "/home/irssi/phenny/beacon.info", "wwwPush@belafonte.us:/home/wwwPush/beacon.info"])

			time.sleep(35)


	targs = (phenny,)
	if singleton.beaconHomeThread is not None and singleton.beaconHomeThread.isAlive():
		singleton.beaconHomePlzStop = True
		singleton.beaconHomeThread.join()
		while singleton.beaconHomeThread.isAlive():
			singleton.beaconHomeThread.join()
		singleton.beaconHomePlzStop = False
	singleton.beaconHomeThread = threading.Thread(target=beaconHome, args = targs)
	singleton.beaconHomeThread.start()




def LEDShift(arduino, fromColor, toColor, timeShift):
	
	print "colors.py - shifting from " + fromColor + " to " + toColor
	def shifttheLED(arduino, fromColor, toColor, timeShift):
		steps = timeShift * 100.0

		fromred = (int(fromColor[0], 16)*16) +  int(fromColor[1], 16)
		fromgreen = (int(fromColor[2], 16)*16) + int(fromColor[3],16)
		fromblue = (int(fromColor[4], 16)*16) + int(fromColor[5],16)
	
		tored = (int(toColor[0], 16)*16) + int(toColor[1], 16)
		togreen = (int(toColor[2], 16)*16) + int(toColor[3], 16)
		toblue = (int(toColor[4], 16)*16) + int(toColor[5], 16)

		diffred = tored - fromred * 1.0
		diffgreen = togreen - fromgreen * 1.0
		diffblue = toblue - fromblue * 1.0

		#print "Diff: " + str(diffred) + " " + str(diffgreen) + " " + str(diffblue)

		redsteps = (diffred / steps) 
		bluesteps = (diffblue / steps) 
		greensteps = (diffgreen / steps) 

		#print "Steps: " + str(redsteps) + " " + str(greensteps) + " " + str(bluesteps)


		#start LED state
		a.analog_write(6, fromred)
		a.analog_write(5, fromgreen)
		a.analog_write(3, fromblue)
	
		for i in range (0, steps):
			#print i

			newred = fromred + (redsteps * i) * 1.0	
			newblue = fromblue + (bluesteps * i) * 1.0
			newgreen = fromgreen + (greensteps * i) * 1.0
			#print "\t " + str(newred) + " " + str(newblue) + " " + str(newgreen)
			#print "\t" + str(redsteps*i) + " " + str(bluesteps*i) + " " + str(greensteps*i) 
	
			a.analog_write(6, int(newred))
			a.analog_write(5, int(newgreen))
			a.analog_write(3, int(newblue))
		
			time.sleep(.01)

	#thread this function
	targs = (arduino, fromColor, toColor, timeShift)
	t = threading.Thread(target=shifttheLED, args=targs)
	t.start()


def setColor(phenny, input):
	global a

	
	if not input.group(2):
		phenny.say("Current color is " + c.currentColor)
		return()
	else:
		if ' ' not in input.group(2):
			newcolor = input.group(2)
			delay = "2"
		else:
			newcolor, delay = input.group(2).split(' ')

        if not input.member:
                phenny.reply("Function reserved for member use")
                return()



	if delay.isdigit():
		if float(delay) < 0 or float(delay) > 1000:
			phenny.say("Innapropriate delay time")
			return()
	else:
		phenny.say("That delay isn't even a number")
		return()

	Valid='1''2''3''4''5''6''7''8''9''10''A''B''C''D''E''F''a''b''c''d''e''f'
	for char in newcolor:
		if char not in Valid:
			phenny.say("Not a valid color - try again")
			return()

	if len(newcolor) != 6:
		phenny.say("Not a valid color - try again")
		return()
				

	phenny.say("Shifting from " + str(c.currentColor) + " to " +  str(newcolor) + " in " + str(delay) + " seconds")

	LEDShift(a, c.currentColor, newcolor, float(delay))

	c.currentColor = newcolor

setColor.commands = ['color']
setColor.priority = 'medium'
setColor.threading = 'True'




