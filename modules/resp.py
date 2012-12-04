"""
responses.py - Reply with default responses

http://inamidst.com/phenny/
Started 11/12/2012 by K. Yankanich
"""

import os
import string
import re

def responses(phenny, input):
	
	conffile = r'responses.conf'
	fn = os.path.join(os.path.expanduser('~/phenny/modules'),  conffile)

	
	asker = input.nick
	question = input.group(0)
	
	
	exclude = set(string.punctuation)
	question = ''.join(ch for ch in question if ch not in exclude)


        result = {}
	f = open(fn)
        for line in f:
		 line = line.strip()
		 if line:
			keyword,reply = line.split(':',1);
        		result[keyword.lower()] = reply
	f.close()

	if result.has_key(question.lower()):
		phenny.reply(result[question.lower()])

	

responses.rule = r'.*'
responses.priority = 'high'

