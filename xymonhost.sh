#!/bin/bash
#
# Checks server to see what xymon hostname should be and sets it
#
# Author: Robert Walker <rw776@york.ac.uk>
#
# Copyright (C) 2015 Robert Walker
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; version 2.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

NEWHOSTNAME="$(wget http://yorkie/echolight.php?key=hostname -q -O -)"
OLDHOSTNAME="$(cat /etc/default/hobbit-client | grep -o 'CLIENTHOSTNAME=.*' | sed "s/CLIENTHOSTNAME=//" | sed "s/\"//g")"
if [ "$OLDHOSTNAME" != "$NEWHOSTNAME" ]
	then
	sed "s/CLIENTHOSTNAME=.*/CLIENTHOSTNAME=\"$NEWHOSTNAME\"/" -i.bak /etc/default/hobbit-client
	service hobbit-client restart
fi
