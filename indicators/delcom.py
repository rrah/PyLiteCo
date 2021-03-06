"""Module for delcom status lights.

Author: Robert Walker <rrah99@gmail.com>

Copyright (C) 2015 Robert Walker

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; version 2.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# Imports
import indicators
import indicators.indicator
import logging
import pywinusb
import pywinusb.hid as hid


logger = logging.getLogger(__name__)


class Device(indicators.indicator.Indicator):
    
    """Delcom Products generation 2 USB device class.
    
    Class attributes:
        _colour_pins (dict): Mapping of colours to pins on device.
        allowed_colours (dict): The colours allowed by this device.
        PRODUCT_ID: Specific indicator id.
        VENDOR_ID: Delcom vendor id.
    
    Instance attributes:
        _current_colour: Which colour is currently on.
        _flashing_pin: Which pin is currently set to flashing.
        device: Pywinusb device for the indicator.
        
    Methods:
        flashing_start: Start the indicator flashing.
        flashing_stop: Stop the indicator flashing.
        read_switch: See if the button has been pressed.
        set_brightness: Change the brightness of the LED's
        set_light: Turn on/off the specified colour.
        set_light_green: Turn on the green LED's.
        set_light_off: Turn off the LED's.
        set_light_red: Turn on the red LED's.
        set_light_yellow: Turn on the yellow LED's.
    """

    # Device Constants
    VENDOR_ID       = 0x0FC5    
    """Delcom Vendor ID."""
    PRODUCT_ID      = 0xB080
    """Delcom Product ID."""
    allowed_colours = {'green': [0x01, 0xFF], 
                                'yellow': [0x04, 0xFF], 
                                'red': [0x02, 0xFF],
                                'orange': [0x06, 0xFF], 
                                'off': [0x00, 0xFF]}
    """Dict matching colour to byte-values."""
    _colour_pins = { 'green'     : 1,
                    'yellow'    : 4,
                    'red'       : 2
                    }
    

    def __init__(self):
        
        """Constructor.
        
        Arguments:
            None.
            
        Returns:
            None.
            
        Raises:
            NoDeviceError.
        """
        
        # Set some default attributes
        self._flashing_pin = None
        self._current_colour = 'off'
        
        filter = hid.HidDeviceFilter(vendor_id = self.VENDOR_ID, product_id = self.PRODUCT_ID)
        try:
            self.device = filter.get_devices()[0]
        except IndexError:
            raise indicators.NoDeviceError
        
        self.device.open()
        
        self._force_off()
        
        # Turn on event counter and reset
        self._write_data(self._make_packet(101, 38, 0x01))
        
        self.set_brightness(50)
    
    def _force_off(self):
        
        """Make sure flashing/LEDs are definitely turned off.
        
        Arguments:
            None
            
        Returns:
            None
        """
        
        self._write_data(self._make_packet(101, 0x0c, 0, 0xFF))
        self._write_data(self._make_packet(101, 20, 1))
        self._write_data(self._make_packet(101, 20, 2))
        self._write_data(self._make_packet(101, 20, 4))        

    def flashing_start(self, flash_speed = 1, colours = 'red'):
        
        """Start the LED's flashing.
        
        Arguments:
            flash_speed (int): Seconds to stay in each state.
                Floored to 0.01 and ceilinged to 2.55
                
        Returns:
            None.
        """
        
        # Get the flash speed in the right range
        if flash_speed > 2.55:
            flash_speed = 2.55
        elif flash_speed < 0.01:
            flash_speed = 0.01
        
        # and change from seconds to value that is given
        # to the device
        flash_speed = int(flash_speed * 100)
        
        # Turn on the relevant LEDs
        self.set_light(colours)
        
        # Set the flash speed and start flashing
        self._write_data(self._make_packet(0x65, 20 + 
                                        self._colour_pins[colours], 
                                        flash_speed, flash_speed))
        self._write_data(self._make_packet(0x65, 20, 0, 
                                            self._colour_pins[colours]))
        
        # Keep track of what pin is flashing
        self._flashing_pin = self._colour_pins[colours]
        
    def flashing_stop(self):
        
        """Check if a pin is actually flashing, and if so
        turn it off and turn off flashing.
        
        Arguments:
            None
        
        Returns:
            None
        """
        
        if self._flashing_pin is not None:
            self.set_light('off')
            self._write_data(self._make_packet(101, 20, 
                                                self._flashing_pin, 0))

    def _make_packet(self, maj_cmd, min_cmd, lsb = 0x00, msb = 0x00):
        
        """Put together a packet to be sent to the device. Pads out packet
        with 0x00 to get it to required size.
        
        Arguments:
            maj_cmd (byte): Major command, as defined in Delcom datasheet.
            min_cmd (byte): Minor command, as defined in Delcom datasheet.
            lsb (byte): Least significant byte for data payload.
            msb (byte): Most significant byte for data payload.
        
        Returns:
            List of 8 bytes, which constitutes a packet.
        """
        
        return [maj_cmd, min_cmd, lsb, msb, 0x00, 0x00, 0x00, 0x00]

    def set_brightness(self, brightness):
        
        """Change brightness of LED's.
        
        Arguments:
            brightness (int): Brightness value between 0 and 100. Below 10 causes flickering.
        
        Returns:
            None
        """
        
        self._set_pwr(brightness)

    def _set_pwr(self, pwr):
        
        """Do the low-level sending of data to change brightness.
        
        Arguments:
            pwr (int): Brightness value between 0 and 100.
            
        Returns:
            None
        """
        
        pwr = int(pwr)
        if pwr > 100:
            pwr = 100
        elif pwr < 0:
            pwr = 0
        self._write_data(self._make_packet(101, 34, 0, pwr))
        self._write_data(self._make_packet(101, 34, 1, pwr))
        self._write_data(self._make_packet(101, 34, 2, pwr))
        
    def _write_data(self, data):
        
        """Send data to the device.
        
        Arguments:
            data (list): list of bytes to send, in the form returned by _make_packet.
            
        Returns:
            None.
        """

        if not self.device.is_plugged():
            raise indicators.NoDeviceError()
        for report in self.device.find_feature_reports():
            if report.report_id == data[0]:
                report[4278190083] = data[1:]
                report.send()

    def read_switch(self):
    
        """See if the button has been pressed.
        
        Arguments:
            None.
        
        Returns: 
            True if pressed, False otherwise.
        """
        
        data = None
        while not data:
            if not self.device.is_plugged():
                raise indicators.NoDeviceError()
            try:
                data = self._read_data(8)
            except hid.HIDError as e:
                # There might be a useful case to see these
                logger.warning(e)
        if data[8:11] == [0, 0, 0]:
            # Bad data, disregard
            return False
        counter = data[0]
        
        if counter > 0:
            return True
        else:
            return False

    def _read_data(self, cmd):
        
        """Get data from the device with the relevant command.
        
        Arguments:
            cmd (int): Command to read, as defined in Delcom datasheet.
            
        Returns:
            Data, as list of bytes.
        """

        reports = self.device.find_feature_reports()
        for report in reports:
            if report.report_id == cmd:
                return report.get()


    def _get_current_colour(self):
        
        """Check what the current colour is.
        
        Arguments:
            None.
            
        Returns:
            Current colour (string).
        """
        
        return self._current_colour
    
    def _set_light(self, colour):
        
        """Change the colour of the light in the indicator.
        
        Arguments:
            colour (string): Colour to set the LED's to.
            
        Returns:
            None
            
        Raises:
            Exception: Colour isn't allowed by device.
        """
    
        # Check it's a colour we can deal with
        if colour not in self.allowed_colours:
            raise Exception('{} - Not allowed colour'.format(colour))
        if self._get_current_colour() == colour:
            # No change
            return
            
        # Make the call to change the colour
        self._write_data(self._make_packet(0x65, 0x0C, 
                                           self.allowed_colours['off'][0], 
                                           self.allowed_colours['off'][1]))
        self._write_data(self._make_packet(0x65, 0x0C, 
                                           self.allowed_colours[colour][0], 
                                           self.allowed_colours[colour][1]))
        
        self._current_colour = colour
        
    def set_light(self, colour):
        
        """Check if flashing and stop flashing, then set colour.
        
        Arguments:
            colour (string): Colour to set the LED's to.
            
        Returns:
            Does not return
        """
        
        if hasattr(self, '_flash_thread'):
            self.flashing_stop()
        self._set_light(colour)

        
    def set_light_red(self):
        
        """Set the LED's to red."""
        
        return self.set_light('red')
        
    def set_light_yellow(self):
        
        """Set the LED's to yellow."""
        
        return self.set_light('yellow')
        
    def set_light_green(self):
        
        """Set the LED's to green."""
        
        return self.set_light('green')

    def set_light_off(self):
        
        """Turn off the LED's."""

        return self.set_light('off')
        
    def __del__(self):
        
        """Stop any flashing and set the light to off at destruction."""
        
        try:
            if self.device.is_open():
                self.flashing_stop()
                self.set_light_off()
                self.device.close()
        except AttributeError:
            # Device wasn't created succesfully
            pass


if __name__ == '__main__':
    import os
    if os.getcwd().split['\\'][-1] is not 'echolight':
        os.chdir('..')
