#!/usr/bin/python

import json

import logging

import echo360.capture_device as echo

import indicators.delcom as delcom

from echoip import ECHO_URL

with open('config.json') as CONFIG_FILE:
    CONFIG = json.load(CONFIG_FILE)

echo_device = echo.Echo360CaptureDevice(ECHO_URL, CONFIG['user'], CONFIG['pass'])
if not echo_device.connection_test.success():
    print('Something went wrong connecting')
else:
    print(echo_device.capture_status_str())


from time import sleep

indi_device = delcom.DelcomGen2()
indi_device.set_light_red()
sleep(1)
indi_device.set_light_off()
