
"""
lusers.py - an attempt to graph the /lusers output on freenode
by Kyle Yankanich because JonathanD poked him too
Hard bits by dwfreed
"""

import os, threading, time, re, singleton
global hiveusers, huserrequest
husers = 0

def setup(phenny):
	def runLuser(phenny):
		while not singleton.lusersPlzStop:
			"""Run Lusers """
			global luserSender, huserrequest
			luserSender = 'log'
			huserrequest = 'log'
			phenny.write(['LUSERS'])
			phenny.write(['WHO', '#hive76', '%nt,1']) 

			time.sleep(600)
	
	targs = (phenny,)
	if singleton.lusersThread is not None and singleton.lusersThread.isAlive():
		singleton.lusersPlzStop = True
		singleton.lusersThread.join()
		while singleton.lusersThread.isAlive():
			singleton.lusersThread.join()
		singleton.lusersPlzStop = False
	singleton.lusersThread = threading.Thread(target=runLuser, args=targs)
	singleton.lusersThread.start()


def lusers(phenny, input):
	global luserSender
	response = input.args[1]
	#trash1, trash2, trash3, users, trash4, max = response.split(' ');
	#users = users[:-1]
	users = response
	if luserSender != 'log':
		if luserSender is not None: 
			phenny.msg(luserSender , users + " users on freenode")
			luserSender = None
	else:
		"""phenny.msg('#hive76bots', 'Gonna write to luser.log')"""
		f = open('/home/irssi/phenny/luser.log', 'a')
		f.write(str(int(time.time())))
		f.write(',' + users + '\n')
		f.close()

	if (int(users) > 85546 and os.path.exists('/home/irssi/FREENODERECORD')):
		os.remove('/home/irssi/FREENODERECORD')
		time.sleep(5)
		phenny.msg('#hive76', "New Freenode user Record has been set! JonathanD, KyleYankan, Peejay, jedijf")
		phenny.msg('#hive76', users + " users on freenode")
		luserSender = '#hive76'
		phenny.write(['LUSERS'])			

	luserSender = None


	

lusers.event = '266'
lusers.rule = r'.*'
lusers.priority = 'medium'


def husercount(phenny, input):
	global husers
	if input.args[1] == '1':
		husers = husers + 1

husercount.event = '354'
husercount.rule = r'.*'
husercount.priority = 'medium'


def huserSend(phenny, input):
	global husers, huserrequest
	if huserrequest != 'log':
		if huserrequest is not None:
			phenny.msg(huserrequest, str(husers) + ' users in ' + huserrequest)
			huserrequest = None
			husers = 0
	else:
                f = open('/home/irssi/phenny/hive76.log', 'a')
                f.write(str(int(time.time())))
                f.write(',' + str(husers) + '\n')
                f.close()
		huserrequest = None
		husers = 0



huserSend.event = '315'
huserSend.rule = r'.*'
huserSend.priority = 'low'





def luserStart(phenny, input):
	global luserSender 
	luserSender = input.sender
	phenny.write(['LUSERS'])			
	

luserStart.commands = ['lusers']
luserStart.priority = 'low'


def huserStart(phenny, input):
	global huserrequest
	huserrequest = input.sender
	phenny.write(['WHO', huserrequest, '%nt,1'])

huserStart.commands = ['huser']
huserStart.priority = 'low'
