"""
Test to test lighting of delcom indicators. Useful for seeing when it throws errors

Author: Robert Walker <rw776@york.ac.uk> 19/03/15
"""
try:
    import os

    if os.getcwd().split('\\')[-1] is not 'echolight':
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

    import indicators.delcom as delcom

    from time import sleep

    logging.info('Starting test')
    device = delcom.DelcomGen2()

    while True:
        logging.debug('Red')
        device.set_light('red')
        sleep(1)
        logging.debug('Yellow')
        device.set_light('yellow')
        sleep(1)
        logging.debug('Green')
        device.set_light('green')
        sleep(1)
        logging.debug('Off')
        device.set_light('off')
        sleep(1)
except KeyboardInterrupt:
    pass
