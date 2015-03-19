#!/usr/bin/python

"""
Module for delcom status lights.

Author: Robert Walker <rw776@york.ac.uk> 19/03/15
"""

import subprocess

import threading

from time import sleep

class DelcomGen2():
    
    def __init__(self):
        self.exe = './control_delcom_gen2.exe'
        self.allowed_colours = {'green': 'green', 
                                'blue': 'blue', 
                                'yellow': 'blue', 
                                'red': 'red', 
                                'off': 'off'}
        self._lock = threading.RLock()
        self.flashing = False

    def set_light(self, colour):
        
        """
        Change the colour of the light in the indicator"""
        
        # Aquire lock
        
        if self.flashing:
            self.set_light_stop_flashing()
        with self:
            # Check it's a colour we can deal with
            if colour not in self.allowed_colours:
                raise Exception('Not allowed colour')
                
            # Make the call to change the colour
            try:
                subprocess.check_call([self.exe, 
                                '--' + self.allowed_colours[colour]])
            except subprocess.CalledProcessError as e:
                # Let's try it again!
                try:
                    subprocess.check_call(e.cmd)
                except subprocess.CalledProcessError as e:
                    # Screw it...
                    raise e
        
    def set_light_red(self):
        
        return self.set_light('red')
        
    def set_light_yellow(self):
        
        return self.set_light('yellow')
        
    def set_light_blue(self):
        
        return self.set_light('blue')
        
    def set_light_green(self):
        
        return self.set_light('green')

    def set_light_off(self):

        return self.set_light('off')
        
    def acquire(self, *args, **kwargs):

        self._lock.acquire(*args, **kwargs)

    def release(self, *args, **kwargs):

        self._lock.release(*args, **kwargs)

    def __enter__(self):

        self.acquire()

    def __exit__(self, type_, value, traceback):

        self.release()


if __name__ == '__main__':
    import os
    if os.getcwd().split['\\'][-1] is not 'echolight':
        os.chdir('..')
