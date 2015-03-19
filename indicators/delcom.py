#!/usr/bin/python

"""
Module for delcom status lights.

Author: Robert Walker <rw776@york.ac.uk> 19/03/15
"""

import subprocess


class DelcomGen2():
    def __init__(self):
        self.exe = '../control_delcom_gen2.exe'
        self.allowed_colours = {'green': 'green', 'yellow': 'blue', 'red': 'red', 'off': 'off'}

    def set_light(self, colour):
        if colour not in self.allowed_colours:
            raise Exception('Not allowed colour')
        subprocess.check_call([self.exe, '--' + self.allowed_colours[colour]])


if __name__ == '__main__':
    from time import sleep
    device = DelcomGen2()
    device.set_light('off')
    sleep(1)
    device.set_light('off')
