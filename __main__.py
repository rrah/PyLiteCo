#!/usr/bin/python

"""
Looks at echo box and changes light depending on state

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
# For freeze
from encodings import hex_codec, utf_8_sig, utf_8, ascii


# Built-in modules
import json
import sys
import logging
import os
from time import sleep


##os.chdir('/usr/local/lib/PyLiteCo')

# Local modules
import echoip
import echo360.capture_device as echo
import indicators.delcom as delcom


def logging_set_up(level = logging.DEBUG, log_file = 'pyliteco.log'):
    
    """
    Set up logging so it prints to console"""

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(filename=log_file, level = level, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')    
    root = logging.getLogger()
    root.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    root.addHandler(ch)
    

def load_config(file_ = 'config.json'):
    
    """
    Try to load the given JSON config file and return data structure"""
    
    try:
        with open(file_) as CONFIG_FILE:
            return json.load(CONFIG_FILE)
    except ValueError:
        logging.exception('Bad config file')    
        
    
def get_light_state_config():
    
    import urllib2
    
    try:
        return json.loads(urllib2.urlopen("http://yorkie/echolight.php?config").read())
    except ValueError:
        logging.error('Could not get configuration from server')
        exit(1)
    
def get_light_action(config_json, device):
    
    """
    Return the method to set the light to what the config file wants"""
    
    # Stop any flashing
    device.flashing_stop()
    
    try:
        if config_json['flash']:
            
            return device.flashing_start(colours = config_json['colour'], flash_speed = config_json['flash_speed'])
        
        if config_json['colour'] == list:
            
            return device.set_light(config_json['colour'][0])
        
        else:
            
            return device.set_light(config_json['colour'])
    except KeyError:
        logging.exception('Bad config file')
        raise
        
    
def check_status(echo_device, indi_device, state_old = None):
    
    """
    Connect to echo box and check state"""
    
    state = [thing.split('=')[1] for thing in echo_device.capture_status_str().split(';') if 'State' in thing][0]
    logging.debug('Echo box in state {}'.format(state))
    if state_old == state: # Avoid unneccesary changes
        return state
    logging.info('Change of state from {} to {}'.format(state_old, state))
    if state in ['inactive', 'active', 'waiting', 'complete', 'paused']:
        try:
            get_light_action(light_state_config[state], indi_device)
        except KeyError:
            logging.exception('Bad light state config')
    else:
        get_light_action(light_state_config['unknown'], indi_device)
        logging.warning('Echo box in unknown state: {}'.format(state))
    return state


def check_button_status(indi_device, echo_device, state = None):
    
    if indi_device.has_been_pressed():
        logging.debug('Button pressed while in state {}'.format(state))
        if state == 'active':
            # recording, so pause
            echo_device.capture_pause()
        elif state == 'paused':
            # paused, so restart
            echo_device.capture_record()

def main():
    
    if sys.platform == 'win32':
        log_file = 'pyliteco.log'
        config_file = 'pyliteco.json'
    else:
        log_file = '/var/log/pyliteco.log'
        config_file = '/etc/pyliteco.json'
    logging_set_up(level = logging.DEBUG)
    
    logging.info('Starting up')
    logging.debug('Running on {}'.format(sys.platform))
    
    
    # Check config definitely exists
    try:
        CONFIG = load_config(config_file)
    except IOError:
        import shutil
        shutil.copyfile('config.json.example', config_file)
        CONFIG = load_config(config_file)
    
    try:
        # Initialise some variables
        error_flash = False
        
        # And the indicator device
        indi_device = delcom.DelcomGen2()
        
        # Loop until connection
        while True:
            global light_state_config
            light_state_config = get_light_state_config()
            logging.info('Loaded light states from server')
            
            # Reload config
            CONFIG = load_config(config_file)
            logging.debug(CONFIG)
            
            # Get ip of echo box
            ECHO_URL = echoip.get_echo_ip()
            logging.info('Got echo url {}'.format(ECHO_URL))
            
            # Try to connect
            echo_device = echo.Echo360CaptureDevice(ECHO_URL, CONFIG['user'], CONFIG['pass'])
            if not echo_device.connection_test.success():
                # Failed to connect, will try again
                logging.error('Something went wrong connecting. Will try again in 10 seconds')
                logging.debug(echo_device.connection_test)
                
                # Check if currently doing error flash and 
                if not error_flash:
                    get_light_action(light_state_config['error'], indi_device)
                    error_flash = True
                sleep(10)
            else:
                # Connected, so (re)set some more variables
                error_flash = False
                state = None
                
                # And loop for status
                while True:
                    try:
                        state = check_status(echo_device, indi_device, state)
                        check_button_status(indi_device, echo_device, state)
                        sleep(1) # For niceness
                    except IndexError:
                        logging.exception('Bad message - lost connection')
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                    except:
                        logging.exception('Something went a little wrong. Continuing loop')
                    
    except KeyboardInterrupt:
        # Someone wants to escape!
        pass
    except:
        logging.exception(None)
        exit(1)
    finally:
        # Bit of cleaning up as delcom throws 
        # some other threads around
        try:
            del indi_device
        except:
            pass
        logging.info('Exiting')
if __name__ == '__main__':
    main()
