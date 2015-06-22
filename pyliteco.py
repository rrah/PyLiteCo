"""Looks at echo box and changes light depending on state

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

# For freeze
from encodings import hex_codec, utf_8_sig, utf_8, ascii


# Built-in modules
import json
import logging
import logging.handlers
import os
import sys
import threading
if sys.platform == 'win32':
    import pywintypes
from time import sleep


# Local modules
import echoip
import echo360.capture_device as echo
import indicators


CONFIG_URL = 'http://yorkie.york.ac.uk/echolight.php'
"""Base URL for gettting config files."""


def logging_set_up(level = logging.DEBUG, log_file = 'pyliteco.log'):
    
    """Set up logging so it prints to console.
    
    Arguements:
        level: Logging level, as defined within the logging module.
        log_file (string): File to dump logs to.
    
    Returns:
        None
    """

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(filename=log_file, level = level, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')    
    root = logging.getLogger()
    root.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    try:
        nthandler = logging.handlers.NTEventLogHandler('pyliteco')
        nthandler.setLevel(level)
        root.addHandler(nthandler)
    except pywintypes.error:
        pass

def load_config(file_ = 'config.json'):
    
    """Get the config from the config file.
    
    Arguements:
        file_ (string): Name of the file to load.
        
    Returns:
        Dict with configuration options.
    """
    
    try:
        with open(file_) as CONFIG_FILE:
            return json.load(CONFIG_FILE)
    except IOError:
        from example import EXAMPLE_CONFIG_JSON as CONFIG
        with open(file_, 'a') as file_:
            json.dump(CONFIG, file_)
    except ValueError:
        logging.exception('Bad config file')
        
    if CONFIG['logging'] in ['INFO', 'DEBUG', 'ERROR', 'WARNING']:
        logging.getLogger().setLevel(eval('logging.{}'.format(CONFIG['logging'])))


def get_light_action(config_json, device):
    
    """Return the method to set the light to what the config file wants.
    
    Arguements:
        config_json (dict): Dictionary containing information for the required light state.
        device (indicators.Device): LED device to set.
        
    Returns:
        Return code of device.set_light method.
    """
    
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
        
    
def check_status(echo_device, indi_device, config, state_old = None):
    
    """
    Connect to echo box and check state"""
    
    state_string = echo_device.capture_status_str()
    logging.debug(state_string)
    state = [thing.split('=')[1] for thing in state_string.split(';') if 'State' in thing][0]
    logging.debug('Echo box in state {}'.format(state))
    if state_old == state: # Avoid unneccesary changes
        return state
    logging.info('Change of state from {} to {}'.format(state_old, state))
    if state in ['inactive', 'active', 'waiting', 'complete', 'paused']:
        try:
            get_light_action(config[state], indi_device)
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

class Main_Thread():
    
    """Thing that does the main running."""
    
    running = False
    
    def __init__(self, config_file, log_file):
        self.arguments = {"config_file_entered":config_file,
                          "log_file_entered":log_file}
        
    def start(self):
        self.running = True
        self.run(**self.arguments)
        
    def is_running(self):
        
        return self.running
    
    def stop(self):
        self.running = False
    
    def run(self, config_file_entered = None, log_file_entered = None):
        
        platform = sys.platform
        if sys.platform == 'win32':
            log_file = 'pyliteco.log'
            config_file = 'pyliteco.json'
        elif platform == 'linux2':
            # Definitely raspbian, maybe others
            log_file = '/var/log/pyliteco.log'
            config_file = '/etc/pyliteco.json'
        else:
            # Catch all the rest and store locally
            log_file = 'pyliteco.log'
            config_file = 'pyliteco.json'
        
        logging_set_up(level = logging.DEBUG, log_file = log_file)
        
        logging.info('Starting up')
        logging.debug('Running on {}'.format(sys.platform))
        
        if config_file_entered is not None:
            config_file = config_file_entered
        if log_file_entered is not None:
            log_file = log_file_entered
        
        
        # Loading of the config
        CONFIG = load_config(config_file)

        try:
            # Initialise some variables
            error_flash = False
            
            # And the indicator device
            indi_device = indicators.get_device(CONFIG['indicator'])()
            
            # Loop until connection
            while self.is_running():              
                # Reload config
                CONFIG = load_config(config_file)
                try:
                    CONFIG.update(echoip.get_echo_config())
                except URLError:
                    pass
                logging.debug(CONFIG)
                
                # Log echo ip
                logging.info('Got echo url {}'.format(CONFIG['ip']))
                
                # Try to connect
                echo_device = echo.Echo360CaptureDevice(CONFIG['ip'], CONFIG['user'], CONFIG['pass'])
                if not echo_device.connection_test.success():
                    # Failed to connect, will try again
                    logging.error('Something went wrong connecting. Will try again in 10 seconds')
                    logging.debug(echo_device.connection_test)
                    
                    # Check if currently doing error flash and 
                    if not error_flash:
                        get_light_action(CONFIG['error'], indi_device)
                        error_flash = True
                    sleep(10)
                else:
                    # Connected, so (re)set some more variables
                    error_flash = False
                    state = None
                    
                    # And loop for status
                    while self.is_running():
                        try:
                            state = check_status(echo_device, indi_device, CONFIG, state)
                            check_button_status(indi_device, echo_device, state)
                        except IndexError:
                            logging.exception('Bad message - lost connection')
                        except KeyboardInterrupt:
                            raise KeyboardInterrupt
                        except:
                            logging.exception('Something went a little wrong. Continuing loop')
                        finally:
                            sleep(1) # Stop the thrashing
                        
        except KeyboardInterrupt:
            # Someone wants to escape!
            pass
        except:
            logging.exception(None)
            sys.exit(1)
        finally:
            # Bit of cleaning up as delcom throws 
            # some other threads around
            try:
                del indi_device
            except:
                pass
            logging.info('Exiting')