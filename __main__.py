"""Main launcher for pyliteco.

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

import logging
import pyliteco
import sys


if __name__ == '__main__':
    
    formatter_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatter_string)
    logging.basicConfig(filename = 'pyliteco.log', format = formatter_string)    
    root = logging.getLogger()
    root.setLevel(logging.NOTSET)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    logger = logging.getLogger(__name__)
    logger.info('Starting up as app.')
    
    import argparse
    
    parser = argparse.ArgumentParser("Start the pyliteco program")
    parser.add_argument('-c', dest = 'config_file', default = None, metavar = 'Config file')
    thread = pyliteco.Main_Thread(**vars(parser.parse_args()))
    thread.start()