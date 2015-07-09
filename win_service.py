"""Set up pyliteco to run as a Windows service.

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

import logging
import os
import pythoncom
import servicemanager
import socket
import sys
import win32serviceutil
import win32service
import win32event
import win32timezone

import pyliteco.pyliteco
import pyliteco.version


class pyliteco_svc (win32serviceutil.ServiceFramework):
    
    """Pyliteco service class.
    
    Attributes:
        _svc_name_ (string): Name for the service.
        _svc_display_name_ (string): Display name for the service.
        _svc_description_ (string): Description for the service.
        _svc_deps_ (list): Dependencies for the service
        
    Methods:
        SvcStop: Run to stop the service.
        SvcDoRun: Code to run when service is running.
    """
    
    _svc_name_ = "pyliteco"
    _svc_display_name_ = "PyLiteCo"
    _svc_description_ = "Service to display Echo box state on Delcom indicator"
    _svc_deps_ = ["EventLog"]

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        
        """Stop the running thread and end the service.
        
        Arguments:
            None
            
        Return:
            None
        """
        
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.thread.stop()

    def SvcDoRun(self):
        
        """Kick off the thread to run the service.
        
        Arguments:
            None
            
        Return:
            None
        """
        
        formatter_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(formatter_string)
        logging.basicConfig(filename = '{}\pyliteco\pyliteco.log'.format(os.environ['PROGRAMFILES']), format = formatter_string)
        root = logging.getLogger()
        nthandler = logging.handlers.NTEventLogHandler('PyLiteCo')
        root.addHandler(nthandler)
        
        root.setLevel(logging.INFO)
        
        logger = logging.getLogger(__name__)
        
        logger.info('Starting up {}'.format(pyliteco.version.VERSION))
        
        self.thread = pyliteco.watchdog.Watchdog_Thread(
                    config_file_entered = '{}\pyliteco\pyliteco.json'.format(
                                                    os.environ['PROGRAMFILES']))
        self.thread.start()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(pyliteco_svc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(pyliteco_svc)