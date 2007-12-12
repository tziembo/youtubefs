#!/usr/bin/env python

import logging
import fuse
import sys
import os
from fuse import Fuse
from youtube.fs.youtubefuse import YoutubeFUSE

fuse.fuse_python_api = (0, 2)

mountError = \
"""
Problem mounting YoutubeFS:
1) Please make sure the target directory is empty
2) YoutubeFS is not already installed
"""
def helpMessage(program):
    msg = "%s youtube_username mountpoint" % program
    print msg
   
if __name__ == "__main__":

    if len(sys.argv) != 3:
        helpMessage(sys.argv[0])
        sys.exit(1)

    try:
        usage = """youtubefs: youtubefs filesystem""" + Fuse.fusage
        server = YoutubeFUSE(version="%prog " + fuse.__version__,
                 usage=usage,dash_s_do='setsingle')
        server.username     = sys.argv[1] 
        server.parse(values=server, errex=1)
        server.main()
    except Exception,inst:
        logging.critical("YoutubeFS main %s",str(inst))
        print mountError 
    
