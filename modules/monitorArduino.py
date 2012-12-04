"""
monitorArduino.py - Nov 2012 KyleYankan

"""


import re, time, threading
from firmata import *

def setup(phenny):
	global a
	a = Arduino('/dev/ttyUSB0')
	a.delay(2)

	def monitorDuino(phenny):

		while True:
			

		targs = (phenny,)
		t = threading.Thread(target=monitorDuino, args = targs)
		t.start()


