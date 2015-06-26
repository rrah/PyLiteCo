"""Deal with config getting/parsing etc.

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


logger = logging.getLogger(__name__)


SERVER = 'yorkie.york.ac.uk/echolight.php'
"""URL (without protocol) for the config server"""
PROTOCOL = 'http'
"""Protocol for connecting to the config server"""
EXAMPLE_CONFIG = '\
{\
    "user": "user",\
    "pass": "pass",\
    "indicator": "dummy",\
    "logging": "INFO",\
    "brightness": "50"\
}'
"""Config normally stored locally. Used to generate local file if none found."""
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
"""Config variables normally got from the server. Don't dump into local config."""
EXAMPLE_CONFIG_JSON = json.loads(EXAMPLE_CONFIG)
"""JSON object representing example settings."""
DEFAULT_CONFIG_JSON = json.loads(DEFAULT_CONFIG)
"""JSON object for default config."""


class EchoipError(Exception):
    
    """When there's an issue getting config from server."""
    
    pass

class BadConfigError(Exception):
    
    """Something wrong with the format of the config."""
    
    def __str__(self):
        return 'Check format of config file.'

def get_config(file_ = 'config.json', url = PROTOCOL + '://' + SERVER):
    
    """Get the config from the file and from the server.
    
    Arguments:
        file_ (string): Location of the local config file.
        url (string): URL for the remote config server.
        
    Returns:
        Config data in JSON style.
    """
    
    try:
        with open(file_) as CONFIG_FILE:
            CONFIG = json.load(CONFIG_FILE)
    except IOError:
        logger.warning('Cannot find config file. Creating new one with defaults.')
        with open(file_, 'a') as open_file:
            json.dump(EXAMPLE_CONFIG_JSON, open_file)
        return get_config(file_)
    except ValueError:
        raise BadConfigError()
    
    try:
        CONFIG.update(get_echo_config())
    except urllib2.URLError:
        logger.warning('Cannot reach config server. Using default settings.')
        CONFIG.update(DEFAULT_CONFIG_JSON)
    except EchoipError:
        logger.warning('Config server refused to return details. Check config server details.\r\n' +
                        '\tUsing default config.')
        CONFIG.update(DEFAULT_CONFIG_JSON)
    
    return CONFIG


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


if __name__ == '__main__':
    print get_echo_config()