#!/usr/bin/python

# Built-in modules
import json
import sys
import logging
from time import sleep


# Local modules
import echoip
import echo360.capture_device as echo
import indicators.delcom as delcom


def logging_set_up(level = logging.DEBUG):
    
    """
    Set up logging so it prints to console"""
    
    root = logging.getLogger()
    root.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    

def load_config(file_ = 'config.json'):
    
    """
    Try to load the given JSON config file and return data structure"""
    
    with open(file_) as CONFIG_FILE:
        return json.load(CONFIG_FILE)
    
    
def check_status(echo_device, indi_device, state_old = None):
    
    """
    Connect to echo box and check state"""
    
    state = [thing.split('=')[1] for thing in echo_device.capture_status_str().split(';') if 'State' in thing][0]
    logging.debug('Echo box in state {}'.format(state))
    if state_old == state: # Avoid unneccesary changes
        return state
    logging.info('Change of state from {} to {}'.format(state_old, state))
    if state == 'inactive':
        indi_device.set_light_off()
    elif state == 'active':
        indi_device.set_light_red()
    elif state == 'waiting':
        indi_device.flashing_start(colours = 'green')
    elif state == 'complete':
        indi_device.flashing_start(colours = 'green')
    elif state == 'paused':
        indi_device.set_light_yellow()
    else:
        indi_device.flashing_start()
    return state


def main():
    logging_set_up(level = logging.DEBUG)
    
    try:
        CONFIG = load_config()
    except IOError:
        import shutil
        shutil.copyfile('config.json.example', 'config.json')
        CONFIG = load_config()
    
    try:
        # Initialise some variables
        error_flash = False
        
        # And the indicator device
        indi_device = delcom.DelcomGen2()
        
        # Loop until connection
        while True:
            ECHO_URL = echoip.get_echo_ip()
            logging.info('Got echo url {}'.format(ECHO_URL))
            echo_device = echo.Echo360CaptureDevice(ECHO_URL, CONFIG['user'], CONFIG['pass'])
            if not echo_device.connection_test.success():
                # Failed to connect, will try again
                logging.error('Something went wrong connecting. Will try again in 10 seconds')
                if not error_flash:
                    indi_device.flashing_start(colours = ['red', 'yellow'])
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
                        sleep(0.5) # For niceness
                    except IndexError:
                        logging.error('Bad message - lost connection')
                        break
                    
    except KeyboardInterrupt:
        # Someone wants to escape!
        pass
    finally:
        # Bit of cleaning up as delcom throws 
        # some other threads around
        del indi_device
    
if __name__ == '__main__':
    main()
