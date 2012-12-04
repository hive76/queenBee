"""
hive76groups.py
created by Kyle Yankanich
Monitors Hive76-discussion on google groups
and posts new topics to the channel
"""
import re, time
import web
import feedparser
import threading, singleton
import json
import urllib
import urllib2


global xmlFeed
xmlFeed = 'https://groups.google.com/group/hive76-discussion/feed/rss_v2_0_topics.xml'

def setup(phenny):
	def RSSCheck(phenny):
		global lastMail	

		feed = feedparser.parse(xmlFeed)
		entries = feed[ "items" ]
		sorted_entries = sorted(entries, key=lambda entry: entry["published_parsed"])
		sorted_entries.reverse()
		lastMail = sorted_entries[0]["title"]	
		
		while not singleton.hive76groupPlzStop:
			feed = feedparser.parse(xmlFeed)	
			entries = feed[ "items" ]
			sorted_entries = sorted(entries, key=lambda entry: entry["published_parsed"])
			sorted_entries.reverse()		

			if (sorted_entries[0]["title"] != lastMail):
				lastMail = sorted_entries[0]["title"]
				phenny.msg('#hive76', "New Group Message: " + lastMail + " by " + sorted_entries[0]["author"] + " - " +  shorten(sorted_entries[0]["link"]) )		
				

	 
			time.sleep(15)


	targs = (phenny,)
	if singleton.hive76groupThread is not None and singleton.hive76groupThread.isAlive():
		singleton.hive76groupPlzStop = True
		singleton.hive76groupThread.join()
		while singleton.hive76groupThread.isAlive():
			singleton.hive76groupThread.join()
		singleton.hive76groupPlzStop = False
	singleton.hive76groupThread = threading.Thread(target=RSSCheck, args=targs)
	singleton.hive76groupThread.start()
 

def MailingList(phenny, input):
	feed = feedparser.parse(xmlFeed)
	entries = feed[ "items" ]
	sorted_entries = sorted(entries, key=lambda entry: entry["published_parsed"])
	sorted_entries.reverse()
	phenny.say("Latest Group Message: " + sorted_entries[0]["title"] + " by " + sorted_entries[0]["author"] + " - " + shorten(sorted_entries[0]["link"]) )


MailingList.commands = ['mail']
MailingList.priority = 'medium'
MailingList.thread = 'true'

def shorten(url):
    gurl = 'https://www.googleapis.com/urlshortener/v1/url'
    req = urllib2.Request(gurl, data= "{\"longUrl\": \"" + url + "\"}" )
    req.add_header('Content-Type', 'application/json')
    results = json.load(urllib2.urlopen(req))
    return results['id']
