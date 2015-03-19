#!/usr/bin/python

import json

import logging

import echo360.capture_device as echo

with open('config.json') as CONFIG_FILE:
    CONFIG = json.load(CONFIG_FILE)

device = echo.Echo360CaptureDevice(CONFIG['server'], CONFIG['user'], CONFIG['pass'])
if not device.connection_test.success():
    print('Something went wrong connecting')

print(device.status_current_capture())
