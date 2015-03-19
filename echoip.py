"""
Get ip for the echobox

Author: Robert Walker <rw776@york.ac.uk> 19/03/15
"""

import urllib2

SERVER = 'http://yorkie/echolight.php'

ECHO_IP = urllib2.urlopen(SERVER).read()

ECHO_URL = 'https://' + ECHO_IP
