"""Looks at echo box and changes light depending on state.

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


# Built-in modules
import json
import logging
import logging.handlers
import sys
import threading
import pywintypes
import pywinusb.hid
import datetime
import time

# Local modules
import pyliteco.config
import echo360.capture_device as echo
import indicators
import pyliteco.watchdog

logger = logging.getLogger(__name__)


class EchoError(Exception):
    
    """Something wrong connecting to echobox"""
    
    pass


def get_light_action(config_json, device):
    
    """Return the method to set the light to what the config file wants.
    
    Arguments:
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
        logger.exception('Bad config file')
        raise
        
    
def check_status(echo_device, indi_device, config, state_old = None):
    
    """Connect to echo box and check state. Do appropriate things based
    on the state.
    
    Arguments:
        echo_device: Echo box object to check state of.
        indi_device: Indicator device to display state on.
        config: Current configuration object.
        state_old (string): Previous state of echo box.
    
    Returns:
        State of echo box, as string.
    """
    
    state_string = echo_device.capture_status_str()
    logger.debug(state_string)
    state = [thing.split('=')[1] for thing in state_string.split(';') if 'State' in thing][0]
    logger.debug('Echo box in state {}'.format(state))
    if state_old == state: # Avoid unneccesary changes
        return state
    logger.info('Change of state from {} to {}'.format(state_old, state))
    if state in ['inactive', 'active', 'waiting', 'complete', 'paused']:
        try:
            get_light_action(config[state], indi_device)
        except KeyError:
            logger.exception('Bad light state config')
    else:
        get_light_action(light_state_config['unknown'], indi_device)
        logger.warning('Echo box in unknown state: {}'.format(state))
    return state


def check_button_status(indi_device, echo_device, state = None):
    
    """Look at the indicator and check if it's been pressed.
    Then take appropriate action.
    
    Arguments:
        indi_device: Indicator object to check status on.
        echo_device: Echo box object to update if button is pressed.
        state: The current state (as known to the program) of the echo box
        
    Returns:
        None
    """
    
    if indi_device.read_switch():
        logger.debug('Button pressed while in state {}'.format(state))
        if state == 'active':
            # recording, so pause
            echo_device.capture_pause()
        elif state == 'paused':
            # paused, so restart
            echo_device.capture_record()


class Main_Thread(threading.Thread):
    
    """Thing that does the main running.
    
    Class Attributes:
        running (bool): Whether the thread is running or not.
        
    Instance Attributes:
        arguements (dict): The arguemenets passed into the constructor.
        
    Methods:
        is_running: Check whether the thread is running.
        load_config: Get the configuration from file/server.
        run: The loop to execute while thread is running.
        start: Set the thread going.
        stop: Signal to stop the thread.
    """
    
    running = False
    
    def __init__(self, kwargs = None):
        
        """Construct the thread with required arguements.
        
        Arguments:
            config_file (string): Location of the local config file.
            
        Returns:
            None.
        """
        
        threading.Thread.__init__(self, target = self.main_loop, kwargs = kwargs)
        self.daemon = True
        self.arguments = kwargs
        
    def _sleep(self, seconds):
        
        """Stop doing execution, but still check flags.
        
        Arguments:
            seconds (int): How long to sleep for
        
        Returns:
            None
        """
        
        while seconds >=0 and self.is_running():
            pyliteco.watchdog.watchdog_queue.put(datetime.datetime.now())
            seconds -= 1
            time.sleep(1)
    
    def is_running(self):
        
        """Check whether the thread should be running.
        
        Arguments:
            None.
        
        Returns:
            True if running, else false.
        """
        
        return self.running
        
    def load_config(self, file_ = 'config.json', old_config = None):
    
        """Get the config from the config file.
        
        Arguments:
            file_ (string): Name of the file to load.
            old_config (dict): Old config to compare new one to.
            
        Returns:
            Dict with configuration options.
        """
        
        CONFIG = pyliteco.config.get_config(file_)
        
        if old_config is not None:
            args = {}
            for thing in CONFIG.keys():
                try:
                    if old_config[thing] != CONFIG[thing]:
                        args[thing] = CONFIG[thing]
                except KeyError:
                    # Not in old config, so a change
                    args[thing] = CONFIG[thing]
            if len(args) == 0:
                # No changes
                return old_config
            
            # Deal with new indicator
            try:
                indicator = args['indicator']
                del self.indi_device
                self.indi_device = indicators.get_device(indicator)()
                self.state = None
                logger.info('Change indicator type to {}.'.format(indicator))
                logger.debug('Reset status to None.')
            except KeyError:
                # No change to indicator
                pass
                
            try:
                brightness = args['brightness']
                self.indi_device.set_brightness(brightness)
            except KeyError:
                # No change to brightness
                pass
            
            # Deal with new echo details
            if set(args.keys()).intersection(set(['user', 'pass', 'ip'])):
                self.echo_device = echo.Echo360CaptureDevice(CONFIG['ip'], CONFIG['user'], CONFIG['pass'])
                if not self.echo_device.connection_test.success():
                    # Failed to connect
                    logger.error('Something went wrong connecting to echo box.')
                    logger.debug(self.echo_device.connection_test)
                    raise EchoError('Unable to connect.')
        
        if CONFIG['logging'] in ['INFO', 'DEBUG', 'ERROR', 'WARNING']:
            logging.getLogger().setLevel(eval('logging.{}'.format(CONFIG['logging'])))
        return CONFIG
    
    def quit(self):
        
        """Forcibly stop the thread.
        
        Arguments:
            None.
        
        Returns:
            None.
        """
        if self.is_running():
            self.stop()
        try:
            del self.indi_device
        except:
            logger.exception('Error closing indicator device.')
        logger.info('Closed pyliteco thread.')
    
    def main_loop(self, config_file_entered = None):
        
        """The main loop for running.
        
        Arguments:
            config_file_entered (string): Location of local config file.
            
        Returns:
            None.
        """
        
        pyliteco.watchdog.watchdog_queue.put(datetime.datetime.now())
        config_file = 'pyliteco.json'
        
        if config_file_entered is not None:
            config_file = config_file_entered
        
        
        # Loading of the config
        CONFIG = self.load_config(config_file)

        try:
            while self.is_running():
                pyliteco.watchdog.watchdog_queue.put(datetime.datetime.now())
                # Initialise some variables
                error_flash = False
                
                # And the indicator device
                try:
                    self.indi_device = indicators.get_device(CONFIG['indicator'])()
                    try:
                        self.indi_device.set_brightness(CONFIG['brightness'])
                    except KeyError:
                        # No brightness in config, use device default
                        pass
                
                    # Loop until connection
                    while self.is_running():
                        pyliteco.watchdog.watchdog_queue.put(datetime.datetime.now())
                        # Reload config
                        try:
                            CONFIG = self.load_config(config_file, CONFIG)
                        except EchoError:
                            self._sleep(60)
                            continue
                        logger.debug(CONFIG)
                        
                        # Log echo ip
                        logger.info('Got echo url {}'.format(CONFIG['ip']))
                        
                        # Try to connect
                        self.echo_device = echo.Echo360CaptureDevice(CONFIG['ip'], CONFIG['user'], CONFIG['pass'])
                        if not self.echo_device.connection_test.success():
                            # Failed to connect, will try again
                            logger.error('Something went wrong connecting to echo box. Will try again in a minute')
                            logger.debug(self.echo_device.connection_test)
                            
                            # Check if currently doing error flash and 
                            if not error_flash:
                                get_light_action(CONFIG['error'], self.indi_device)
                                error_flash = True
                            self._sleep(60)
                        else:
                            # Connected, so (re)set some more variables
                            error_flash = False
                            self.state = None
                            count = 0
                            
                            # And loop for status
                            while self.is_running():
                                pyliteco.watchdog.watchdog_queue.put(datetime.datetime.now())
                                try:
                                    if count < 60:
                                        count += 1
                                    else:
                                        logger.debug('Reloading config')
                                        CONFIG = self.load_config(config_file, CONFIG)
                                        count = 0
                                    self.state = check_status(self.echo_device, self.indi_device, CONFIG, self.state)
                                    check_button_status(self.indi_device, self.echo_device, self.state)
                                except EchoError:
                                    break
                                except IndexError:
                                    logger.exception('Bad message - lost connection to echo box.')
                                finally:
                                    self._sleep(1) # Stop the thrashing
                except indicators.NoDeviceError:
                    logger.error('Can not connect to device. Check config and check it is plugged in.')
                finally:
                    self._sleep(10)
                        
        except KeyboardInterrupt:
            # Someone wants to escape!
            pass
        except:
            logger.exception(None)
        finally:
            self.quit()
            
    def start(self, *args, **kwargs):
        
        self.running = True
        threading.Thread.start(self, *args, **kwargs)
        
    def stop(self):
        
        """Set attribute so thread stops running.
        
        Arguments:
            None.
            
        Returns:
            None.
        """
        
        self.running = False
        
    