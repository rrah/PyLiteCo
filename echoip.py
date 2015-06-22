#!/usr/bin/python

"""
Grab the ip of the echo box from a server 

Author: Robert Walker <rrah99@gmail.com>

Copyright (C) 2015 Robert Walker

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; version 2.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import json
import logging
import urllib2
import sys

logging.getLogger()

SERVER = 'yorkie.york.ac.uk/echolight.php'
PROTOCOL = 'http'


def get_echo_ip():
    return urllib2.urlopen(PROTOCOL + '://' + SERVER).read()

def get_light_state_config():
    
    try:
        return json.loads(urllib2.urlopen(PROTOCOL + '://' + SERVER + "?config").read())
    except ValueError:
        logging.error('Could not get configuration from server')
        sys.exit(1)
        
def get_echo_config():
    
    config = get_light_state_config()
    config.update({'ip': 'https://' + get_echo_ip()})
    return config