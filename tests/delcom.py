#!/usr/bin/python

"""
Test to test lighting of delcom indicators. Useful for seeing when it throws errors

Author: Robert Walker <rw776@york.ac.uk>

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

try:
    import os

    if os.getcwd().split('/')[-1] != 'echolight':
        os.chdir('..')

    import sys

    import logging

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    # PATH for packages
    sys.path.append('.')

    from time import sleep

    logging.info('Starting test')
    
    import indicators.delcom as delcom
    device = delcom.DelcomGen2()
    while True:
        
        for colour in device.allowed_colours:
            logging.info('steady {}'.format(colour))
            device.set_light(colour)
            sleep(1)
        
        logging.info('flash fast red for 5 seconds')
        device.set_light_red()
        device.flashing_start(0.2, 'red')
        sleep(5)
        device.flashing_stop()
        
        logging.info('flash slow green for 5 seconds')
        device.set_light_red()
        device.flashing_start(1, 'green')
        sleep(5)
        device.flashing_stop()

except KeyboardInterrupt:
    device.flashing_stop()
