#!/usr/bin/env python

import fuse
import sys
import os
from fuse import Fuse
from youtube.fs.youtubefuse import YoutubeFUSE

fuse.fuse_python_api = (0, 2)

def helpMessage(program):
    msg = "%s youtube_username mountpoint" % program
    print msg
    
if __name__ == "__main__":
    usage = """
Userspace nullfs-alike: mirror the filesystem tree from some point on.

""" + Fuse.fusage

    server = YoutubeFUSE(version="%prog " + fuse.__version__,
                 usage=usage,dash_s_do='setsingle')
    
    server.username     = "tanuvishu"
    server.parse(values=server, errex=1)
    server.main()

    
