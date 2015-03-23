#!/usr/bin/python
try:
    import os

    if os.getcwd().split('/')[-1] != 'echolight':
        os.chdir('..')

    import sys

    import logging

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    # PATH for packages
    sys.path.append('.')

    from time import sleep

    logging.info('Starting test')
    
    import indicators.delcom as delcom
    device = delcom.DelcomGen2()
    while True:
        print device.read()
        sleep(1)        

except KeyboardInterrupt:
    device.flashing_stop()
