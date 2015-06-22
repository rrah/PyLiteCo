"""Example config json to create file if none is avaliable.

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

EXAMPLE_CONFIG = '\
{\
    "user": "user",\
    "pass": "pass",\
    "indicator": "dummy",\
    "logging": "INFO"\
}'
"""String in JSON form of example settings."""

EXAMPLE_CONFIG_JSON = json.loads(EXAMPLE_CONFIG)
"""JSON object representing example settings."""