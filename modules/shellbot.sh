#!/usr/bin/env bash
# shellbot.sh - IRC Bot
# Author: Sean B. Palmer, inamidst.com

NICK=shellbotKyle2
SERVER=${1:-irc.freenode.org}
CHANNEL=${2:-#hive76bots}

echo "NICK $NICK" > shellbot.input
echo "USER $(whoami) +iw $NICK :$0" >> shellbot.input
echo "CAP REQ :account-notify extended-join" >> shellbot.input
echo "JOIN $CHANNEL" >> shellbot.input
echo "WHO #hive76bots %na" >> shellbot.input

tail -f shellbot.input | telnet $SERVER 6667 | \
   while true
   do read LINE || break

      echo $LINE
      if echo $LINE | egrep "$NICK: ping$" &> /dev/null
      then echo "PRIVMSG $CHANNEL :pong" >> shellbot.input
      fi
   done

# [EOF]
