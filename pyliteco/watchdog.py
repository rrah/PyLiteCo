"""Watch the main thread and restart if it hangs.

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
import pyliteco.pyliteco
import queue
import threading

from time import sleep

logger = logging.getLogger(__name__)

watchdog_queue = queue.Queue()

class Watchdog_Thread(object):
    
    
    def __init__(self, **args):
        
        """Construct the thread with required arguements.
        
        Arguements:
            config_file (string): Location of the local config file.
            
        Returns:
            None.
        """
        
        self._args = args
    
    def is_running(self):
        
        """Check whether the thread should be running.
        
        Arguements:
            None.
        
        Returns:
            True if running, else false.
        """
        
        return self.running
    
    def run(self):
        
        logger.info('Starting watchdog thread')
        self.pyliteco_thread = pyliteco.pyliteco.Main_Thread(kwargs = self._args)
        self.pyliteco_thread.start()
        while self.is_running():
            try:
                watchdog_queue.get(True, 100)
                logger.debug('Got message from pyliteco thread.')
            except queue.Empty:
                # Nothing's been added to the queue in 10 seconds, thread has hung
                logger.warning('pyliteco thread hung, restarting.')
                self.pyliteco_thread.quit()
                self.pyliteco_thread = pyliteco.pyliteco.Main_Thread(kwargs = self._args)
                self.pyliteco_thread.start()
        self.pyliteco_thread.running = False
        self.pyliteco_thread.join()
        logger.info('Closing watchdog thread')
        
    def start(self):
        
        """Set off the thread running.
        
        Arguements:
            None.
            
        Returns:
            None.
        """
        
        self.running = True
        self.run()
        
    def stop(self):
        
        """Set attribute so thread stops running.
        
        Arguements:
            None.
            
        Returns:
            None.
        """
        
        self.running = False