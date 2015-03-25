#!/bin/bash

NEWHOSTNAME="$(wget http://yorkie/echolight.php?key=hostname -q -O -)"
OLDHOSTNAME="$(cat /etc/default/hobbit-client | grep -o 'CLIENTHOSTNAME=.*' | sed "s/CLIENTHOSTNAME=//" | sed "s/\"//g")"
if [ "$OLDHOSTNAME" != "$NEWHOSTNAME" ]
	then
	sed "s/CLIENTHOSTNAME=.*/CLIENTHOSTNAME=\"$NEWHOSTNAME\"/" -i.bak /etc/default/hobbit-client
	service hobbit-client restart
fi
