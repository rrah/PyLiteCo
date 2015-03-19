#!/usr/bin/python

import json

import logging

import echo360.capture_device as echo

import indicators.delcom as delcom

with open('config.json') as CONFIG_FILE:
    CONFIG = json.load(CONFIG_FILE)

print CONFIG

echo_device = echo.Echo360CaptureDevice(CONFIG['server'], CONFIG['user'], CONFIG['pass'])
if not echo_device.connection_test.success():
    print('Something went wrong connecting')

print(echo_device.status_system())
