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

from pywinusb import hid
from time import sleep
from random import randint

def thingy(data):
    if data[8:11] == [0, 0, 0]:
        return
    for i in range(data[0]):
        print 'Pressed!'
        _write_data(indicator, _make_packet(101, 0x0c, randint(0, 7), 0xFF))
    
def _make_packet(maj_cmd, min_cmd, lsb = 0x00, msb = 0x00):
        
    return [maj_cmd, min_cmd, lsb, msb, 0x00, 0x00, 0x00, 0x00]

    
def _write_data(device, data):

    for report in device.find_feature_reports():
        if report.report_id == data[0]:
            report[4278190083L] = data[1:]
            report.send()

filter = hid.HidDeviceFilter(vendor_id = 0x0FC5, product_id = 0xB080)

indicator = filter.get_devices()[0]

indicator.open()
try:

    indicator.set_raw_data_handler(thingy)
    
    _write_data(indicator, _make_packet(101, 8, 0x01))
    
    print "Activated button"
    while True:
        sleep(0.1)
        for report in indicator.find_feature_reports():
            if report.report_id == 0x08:
                try:
                    report.get()
                except:
                    pass
finally:      
    indicator.close()

exit()