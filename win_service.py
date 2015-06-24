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
import pythoncom
import servicemanager
import socket
import sys
import win32serviceutil
import win32service
import win32event

import pyliteco
from logging import NOTSET


class pyliteco_svc (win32serviceutil.ServiceFramework):
    _svc_name_ = "pyliteco"
    _svc_display_name_ = "PyLiteCo"
    _svc_description_ = "Service to display Echo box state on Delcom indicator"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.thread.stop()

    def SvcDoRun(self):
        root = logging.getLogger()
        nthandler = logging.handlers.NTEventLogHandler('PyLiteCo', 
                        dllname = 'C:\\Program Files (x86)\\pyliteco\\pyliteco-service.exe')
        root.addHandler(nthandler)
        
        root.setLevel(logging.NOTSET)
        
        logging.info('Starting up')
        
        self.thread = pyliteco.Main_Thread("C:\Program Files (x86)\pyliteco\pyliteco.json", 
                                           "C:\Program Files (x86)\pyliteco\pyliteco.log")
        self.thread.start()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(pyliteco_svc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(pyliteco_svc)