#!/usr/bin/python

import json

import logging

import echo360.capture_device as echo

with open('config.json') as CONFIG_FILE:
    CONFIG = json.loads(CONFIG)

device = echo.Echo360CaptureDevice(CONFIG['server'], CONFIG['user'], CONFIG['pass'])
