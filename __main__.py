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


from echoip import ECHO_URL


with open('config.json') as CONFIG_FILE:
    CONFIG = json.load(CONFIG_FILE)

indi_device = delcom.DelcomGen2()
echo_device = echo.Echo360CaptureDevice(ECHO_URL, CONFIG['user'], CONFIG['pass'])

def check_status():
    if not echo_device.connection_test.success():
        logging.error('Something went wrong connecting')
    else:
        state = [thing.split('=')[1] for thing in echo_device.capture_status_str().split(';') if 'State' in thing][0]
        if state == 'inactive':
            indi_device.set_light_off()
        elif state == 'active':
            indi_device.set_light_red()
        else:
            indi_device.start_flashing()
try:
    while True:
        check_status()
        sleep(0.5)
except KeyboardInterrupt:
    pass
