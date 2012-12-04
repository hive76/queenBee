"""
exclaim.py - Phenny Yell Module

http://inamidst.com/phenny/
"""

def interjection(phenny, input):
        phenny.say(input.nick + '!')
interjection.rule = r'$nickname!'
interjection.priority = 'high'

