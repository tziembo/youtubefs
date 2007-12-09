#!/usr/bin/env python
__author__      = "Vishal Patil"
__copyright__   = "Copyright 2007 - 2008, Vishal Patil"
__license__     = "MIT"

import logging
import threading
import re

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='youtube.fs.log',
                    filemode='w')

class counter:
    def __init__(self, start=0, increment=1):
        self.counter = start
        self.increment = increment
        self.lock = threading.RLock()

    def next(self):
        self.lock.acquire()
        self.counter += self.increment
        i = self.counter
        self.lock.release()
        return i

YoutubeInodeCounter = counter(0,1)
