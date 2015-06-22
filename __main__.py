#!/usr/bin/python

"""
Main launcher for pyliteco

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

import pyliteco

from time import sleep

if __name__ == '__main__':
    
    import argparse
    
    parser = argparse.ArgumentParser("Start the pyliteco program")
    parser.add_argument('-c', dest = 'config_file', default = None, metavar = 'Config file')
    parser.add_argument('-l', dest = 'log_file', default = None, metavar = 'Log file')
    thread = pyliteco.Main_Thread(**vars(parser.parse_args()))
    thread.start()