#!/usr/bin/python

"""
Module for delcom status lights.

Author: Robert Walker <rw776@york.ac.uk> 19/03/15
"""

# Builtin imports
import threading
import sys
import logging
from time import sleep


# Does communication to usb. Surprisingly
import usb


class DelcomGen2(object):
    '''
    Class for talking to Delcom Products generation 2 USB device 
    Modified from http://permalink.gmane.org/gmane.comp.python.pyusb.user/91
    '''

    # Device Constants
    VENDOR_ID       = 0x0FC5    #: Delcom Product ID
    PRODUCT_ID      = 0xB080    #: Delcom Product ID
    INTERFACE_ID    = 0         #: The interface we use
    allowed_colours = {'green': '\x01\xFF', 
                                'yellow': '\x04\xFF', 
                                'red': '\x02\xFF',
                                'orange': '\x03\xFF', 
                                'off': '\x00\xFF'}

    def __init__(self):
        '''
        Constructor'''
        
        self.device = usb.core.find(idProduct = self.PRODUCT_ID)
        try:
            self.device.detach_kernel_driver(0)
        except:
            pass
        self.device.set_configuration()
        self._current_colour = 'off'
        
        self.set_light_off()

    def _flash(self, flash_speed = 1, colours = 'red'):
        
        """
        function for flash thread to run"""
        
        if type(colours) is list:
            flash_list = colours
        else:
            flash_list = [colours, 'off']
        
        while self._flashing:
            for colour in flash_list:
                self._set_light(colour)
                sleep(flash_speed)
        return

    def flashing_start(self, flash_speed = 1, colours = 'red'):
        
        """
        flash_speed = how long to spend on each step of the flash
                        default: 1
        colours = what colour(s) to flash. If list flash between, 
                    otherwise on/off that colour.
                        default: red
        """
        
        kwargs = {'flash_speed':flash_speed, 
                    'colours': colours}
        if hasattr(self, '_flash_thread'):
            self.flashing_stop
        self._flashing = True
        self._flash_thread = threading.Thread(target = self._flash, kwargs = kwargs)
        self._flash_thread.daemon = True
        self._flash_thread.start()
        
    def flashing_stop(self):
        
        if hasattr(self, '_flash_thread'):
            self._flashing = False
            self._flash_thread.join()
            del self._flash_thread

        
    def _write_data(self, data):

        self.device.ctrl_transfer(0x21, 0x09, 0x0365, 0x0000, data, 100)

    def _read_data(self):

        packet = '\x64\x00\x00\x00\x00\x00\x00\x00'
        data = self.device.ctrl_transfer(0xA1, 0x08, 0x0064, 0x0000, 8)
        return data
                                    
    def read(self):
        
        return self._read_data()


    def _get_current_colour(self):
        
        return self._current_colour
    
    def _set_light(self, colour):
        
        """
        Change the colour of the light in the indicator"""
    
        # Check it's a colour we can deal with
        if colour not in self.allowed_colours:
            raise Exception('{} - Not allowed colour'.format(colour))
        if self._get_current_colour() == colour:
            # No change
            return
            
        # Make the call to change the colour
        msg = "\x65\x0C{}\x00\x00\x00\x00".format(self.allowed_colours[colour])
        self._write_data("\x65\x0C\x00\xFF\x00\x00\x00\x00")
        self._write_data(msg)
        
        self._current_colour = colour
        
    def set_light(self, *args, **kwargs):
        
        """
        Check if flashing and stop flashing"""
        
        if hasattr(self, '_flash_thread'):
            self.flashing_stop()
        self._set_light(*args, **kwargs)

        
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
        
    def __del__(self):
        
        """
        Stop any flashing and set the light to off at
        destruction"""
        
        self.flashing_stop()
        self.set_light_off()


class DeviceDescriptor(object):
    '''
    Class for defining the USB device
    '''

    def __init__(self, vendor_id, product_id, interface_id):
        '''
        Constructor
        '''
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.interface_id = interface_id

    def getDevice(self):
        '''
        Return the device corresponding to the device descriptor if it is
        available on the USB bus.  Otherwise return None.  Note that the
        returned device has yet to be claimed or opened.
        '''
        # Find all the USB busses
        busses = usb.busses()
        for bus in busses:
            for device in bus.devices:
                if device.idVendor == self.vendor_id and \
                   device.idProduct == self.product_id:
                    return device
        return None

if __name__ == '__main__':
    import os
    if os.getcwd().split['\\'][-1] is not 'echolight':
        os.chdir('..')
