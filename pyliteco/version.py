"""Holds version variables for PyLiteCo.

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

import argparse


maj_ver = 1
min_ver = 4
patch_ver = 2
rc_ver = 1

VERSION = '{}.{}.{}'.format(maj_ver, min_ver, patch_ver)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Get the version for PyLiteCo.')
    parser.add_argument('--rc', dest = 'rc', action = 'store', default = False, type = bool)
    args = parser.parse_args()
    ret_val = VERSION.replace('.', '-')
    if args.rc:
        ret_val += '-rc-{}'.format(rc_ver)
    print(ret_val)