#!/usr/bin/env python

import fuse
import sys
import os
from fuse import Fuse
from youtube.fs.youtubefuse import YoutubeFUSE

fuse.fuse_python_api = (0, 2)

fuse.feature_assert('stateful_files', 'has_init')

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
    server.parser.add_option(mountopt="root", metavar="PATH", default='/', \
                             help="mirror filesystem from under PATH [default: %default]")
    server.parse(values=server, errex=1)

    try:
        if server.fuse_args.mount_expected():
            os.chdir(server.root)
    except OSError:
        print >> sys.stderr, "can't enter root of underlying filesystem"
        sys.exit(1)

    server.main()

    
