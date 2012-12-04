#!/usr/bin/perl

#1353303800      #hive76bots     KyleYankan      Bed
#EPOCHDATE	CHANNEL	 	NICK	MESSAGE

use JSON;
use LWP::Simple;
use DateTime::Format::ISO8601;

$now = DateTime->now;
$timemin = $now->iso8601;
print "$timemin\n";

$then = $now;
$then->add( years => 1 );
$timemax = $then->iso8601;
print "$timemax\n";

$calURL = 'https://www.googleapis.com/calendar/v3/calendars/hive76.org_b6up588cfkui85d83v5oekhvco%40group.calendar.google.com/events?singleEvents=true&key=AIzaSyCkr1uIFuY4Ovh4Bj6qoO-BhUnq6VKnlqk&timeMin=' . $timemin . '-05:00&timeMax=' . $timemax . '-05:00';

print $calURL . "\n";

$reqJSON = get($calURL);
die "Couldn't get the Calendar Feed: $!" unless defined $reqJSON;

$calendar = {};
$events = 0;

$calendar = decode_json $reqJSON;
$events =  scalar( $calendar->{"items"} );
@calendar = $calendar->{"items"};



print $calendar->{"updated"} . "\n";

print "localtime: " . $now->epoch() . "\n";

open(FILE, ">/home/irssi/.phenny/QueenBee-irc.freenode.org.events.db") or die "Can't open file: $!\n";

for my $event ( @{$calendar->{"items"}} ) {

	if ($event->{"start"}->{"dateTime"} =~ /T/) {

		my $start = DateTime::Format::ISO8601->parse_datetime( $event->{"start"}->{"dateTime"});
		my $end = DateTime::Format::ISO8601->parse_datetime( $event->{"end"}->{"dateTime"});

		#$timeDiff = $end->delta_ms($start);

			#print $event->{"summary"} . " @ " . $start->datetime() . " to " . $end->datetime() . "\n";
			#print "\t " . $event->{"description"} . " at " . $event->{"location"}. "\n";
			#print "\n";

			#print $start->epoch() . " < " . $now->epoch() . " == ". localtime() . "\n";

			#Put into reminders file
		
			print FILE $start->epoch() . "\t#hive76bots\tEveryone\t " . $event->{"summary"} . "\n";	

		
	}

}

close(FILE);
