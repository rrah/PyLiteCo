"""Example and default config json's to use if none are avaliable.

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

DEFAULT_CONFIG = '''
{
    "ip": "127.0.0.1",
    "active": {
            "colour": "red",
            "flash": false,
            "flash_speed": 1
    },
    "inactive": {
            "colour": "off",
            "flash": false,
            "flash_speed": 1
    },
    "complete": {
            "colour": "green",
            "flash": true,
            "flash_speed": 1
    },
    "waiting": {
            "colour": "off",
            "flash": false,
            "flash_speed": 1
    },
    "paused": {
            "colour": "yellow",
            "flash": false,
            "flash_speed": 1
    },
    "error": {
            "colour": "off",
            "flash": false,
            "flash_speed": 1
    },
    "unknown": {
            "colour": "off",
            "flash": false,
            "flash_speed": 1
    }
}
'''

DEFAULT_CONFIG_JSON = json.loads(DEFAULT_CONFIG)