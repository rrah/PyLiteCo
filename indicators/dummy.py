"""Dummy indicator that logs stuff when things happen.

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

import indicators.indicator
import logging


logger = logging.getLogger(__name__)


class Device(indicators.indicator.Indicator):
    
    """Pretends to be an indicator so stuff can be tested.
    
    Class attributes:
        None.
        
    Instance attributes:
        None.
    
    Methods:
        flashing_start: Pretend to start flashing.
        flashing_stop: Pretend to stop flashing.
        read_switch: Pretend to check button status.
        set_brightness: Pretend to change the brightness.
        set_light: Pretend to turn on/off a specific colour.
    """
    
    def _report(self, msg):
        
        logger.info(msg)
        
    def flashing_start(self, colours, flash_speed):
        
        """Report the start of flashing.
        
        Arguments:
            colours: Doesn't matter, ignored.
            flash_speed: Doesn't matter, ignored.
            
        Returns:
            None.
        """
        
        self._report('Starting flashing')
        
    def flashing_stop(self):
        
        """Report the end of flashing.
        
        Arguments:
            None.
            
        Returns:
            None.
        """
        
        self._report('Stopping flashing')
        
    def read_switch(self):
        
        """Never gonna give you UP, never gonna let you DOWN.
        
        Arguments:
            None.
        
        Return:
            False. Always.
        """
        
        return False
    
    def set_brightness(self, brightness):
        
        """Baby, you light up my world.
        
        Arguments:
            brightness (int): Eh, basically ignored.
            
        Return:
            None.
        """
        
        pass
        
    def set_light(self, colour):
        
        """Report the setting of a colour.
        
        Arguments:
            colour (string): Anything, is ignored.
            
        Returns:
            None.
        """
        
        self._report('Set to {}'.format(colour))