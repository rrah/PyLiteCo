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

def _get_file(url):
    
    """Wrapper to grab a file and raise an exception if the file
    is not valid.
    
    Arguements:
        url (string): URL to get the file from.
        
    Returns:
        file_ (string): Body of the file.
    """
    
    file_ = urllib2.urlopen(url).read()
    if file_ == '404' or file_ == '':
        raise EchoipError('Server returned 404')
    else:
        return file_


def get_echo_ip():
    
    """Get the IP this indicator should be looking at.
    
    Returns:
        ip (string): String containing the IP
    """
    
    return _get_file(PROTOCOL + '://' + SERVER)

def get_light_state_config():
    
    return json.loads(_get_file(PROTOCOL + '://' + SERVER + "?config"))
        
def get_echo_config():
    
    config = get_light_state_config()
    config.update({'ip': 'https://' + get_echo_ip()})
    return config

class EchoipError(Exception):
    
    pass

if __name__ == '__main__':
    print get_echo_config()