#!/usr/bin/python

"""
Test the reading from the delcom device

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
        print device.has_been_pressed()
        sleep(3)

except KeyboardInterrupt:
    device.flashing_stop()
