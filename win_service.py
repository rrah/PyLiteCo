"""
Set up pyliteco to run as a Windows service
Author: Robert Walker <rw776@york.ac.uk>
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

import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket


from pyliteco import main


class pyliteco_svc (win32serviceutil.ServiceFramework):
    _svc_name_ = "pyliteco"
    _svc_display_name_ = "PyLiteCo"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        main()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(pyliteco_svc)