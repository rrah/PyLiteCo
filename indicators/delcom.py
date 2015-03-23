#!/usr/bin/python

"""
Module for delcom status lights.

Author: Robert Walker <rw776@york.ac.uk> 19/03/15
"""

import subprocess

import threading

import usb
import sys

import logging

from time import sleep


class DelcomGen2(object):
    '''
    Class for talking to Delcom Products generation 2 USB device 
    Modified from http://permalink.gmane.org/gmane.comp.python.pyusb.user/91
    '''

    # Device Constants
    VENDOR_ID       = 0x0FC5    #: Delcom Product ID
    PRODUCT_ID      = 0xB080    #: Delcom Product ID
    INTERFACE_ID    = 0         #: The interface we use

    def __init__(self):
        '''
        Constructor
        '''
        self.deviceDescriptor = DeviceDescriptor(self.VENDOR_ID, 
                                                 self.PRODUCT_ID, 
                                                 self.INTERFACE_ID)
        self.device = self.deviceDescriptor.getDevice()
        if self.device:
            self.conf = self.device.configurations[0]
            self.intf = self.conf.interfaces[0][0]
        else:
            logging.error("Cable isn't plugged in")
        self.allowed_colours = {'green': '\x01\xFF', 
                                'yellow': '\x04\xFF', 
                                'red': '\x02\xFF',
                                'orange': '\x03\xFF', 
                                'off': '\x00\xFF'}
        self._current_colour = 'off'
        
        self.open()
        self.writeData("\x65\x0C\x00\xFF\x00\x00\x00\x00")
        self.close()

    def _flash(self, flash_speed = 1, colours = 'red'):
        
        if type(colours) is list:
            flash_list = colours
        else:
            flash_list = [colours, 'off']
        
        flash_colour = self._get_current_colour()
        
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
    
    def open(self):
        
        """ 
        Open the Delcom Interface """
        
        self.handle = self.device.open()
        try:
            self.handle.detachKernelDriver(0)
        except:
            pass
        self.handle.claimInterface(self.intf) # Interface 0   

    def close(self):
        
        """ 
        Release Delcom interface """
        
        try:
            self.handle.releaseInterface()
        except Exception, err:
            logging.error(sys.stderr, err)

    def getManufactureName(self):
        """ Manufacturer of device """
        return self.handle.getString(self.device.iManufacturer,30)

    
    def getProductName(self):
        """ Product name of device """
        return self.handle.getString(self.device.iProduct,30)

        
    def writeData(self, data):
        """ 
        Write data to device:
                0x21   = REQ_TYPE: DIR = Host to Device
                         REQ_TYPE: TYPE = Class
                         REQ_TYPE: REC = Interface
                0x09   = REQUEST: HID-Set Report
                data   = Command sent to Delcom device
                0x0365 = VALUE: 0x65 = ReportID = 101 = MajorCMD
                         VALUE: 0x03 = Report Type = Feature Report
                0x0000 = Interface number = 0
                100    = timeout 100mS
        """

        sent = self.handle.controlMsg(0x21,
                                      0x09,
                                      data,
                                      0x0365,
                                      0x0000,
                                      100)      
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
        self.open()
        msg = "\x65\x0C{}\x00\x00\x00\x00".format(self.allowed_colours[colour])
        self.writeData("\x65\x0C\x00\xFF\x00\x00\x00\x00")
        self.writeData(msg)
        self.close()
        
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
