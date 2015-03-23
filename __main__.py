#!/usr/bin/python


import json
import sys
from time import sleep


import logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


import echo360.capture_device as echo
import indicators.delcom as delcom
import echoip

with open('config.json') as CONFIG_FILE:
    CONFIG = json.load(CONFIG_FILE)

indi_device = delcom.DelcomGen2()

def check_status(state_old = None):
        state = [thing.split('=')[1] for thing in echo_device.capture_status_str().split(';') if 'State' in thing][0]
        logging.debug('Echo box in state {}'.format(state))
        if state_old == state:
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
        else:
            indi_device.flashing_start()
        return state
try:
    # Initialise some variables
    error_flash = False
    while True:
        ECHO_URL = echoip.get_echo_ip()
        logging.info('Got echo url {}'.format(ECHO_URL))
        echo_device = echo.Echo360CaptureDevice(ECHO_URL, CONFIG['user'], CONFIG['pass'])
        if not echo_device.connection_test.success():
            logging.error('Something went wrong connecting. Will try again in 10 seconds')
            if not error_flash:
                indi_device.flashing_start(colours = ['red', 'yellow'])
                error_flash = True
            sleep(10)
        else:
            error_flash = False
            state = None
            while True:
                state = check_status(state)
                sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    del indi_device
    
