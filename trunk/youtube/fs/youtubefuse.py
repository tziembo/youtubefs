#!/usr/bin/env python
__author__      = "Vishal Patil"
__copyright__   = "Copyright 2007 - 2008, Vishal Patil"
__license__     = "MIT"


import sys
from fuse import Fuse
from youtube.api.protocol import YoutubeVideo
from youtube.api.protocol import YoutubePlaylist
from youtube.api.protocol import YoutubeUser

class YoutubeFS(Fuse):
    """
    
    """
    def __init__(self, *args, **kw):
        Fuse.__init__(self, *args, **kw)
        logging.debug('YoutubeFS: Init complete')

    def getattr(self, path):
        """
        - st_mode (protection bits)
        - st_ino (inode number)
        - st_dev (device)
        - st_nlink (number of hard links)
        - st_uid (user ID of owner)
        - st_gid (group ID of owner)
        - st_size (size of file, in bytes)
        - st_atime (time of most recent access)
        - st_mtime (time of most recent content modification)
        - st_ctime (platform dependent; time of most recent metadata change on Unix,
                    or the time of creation on Windows).
        """

        logging.debug('YoutubeFS: getattr ' + path)
        return -errno.ENOSYS

    def getdir(self, path):
        """
        return: [('file1', 0), ('file2', 0), ... ]
        """
        logging.debug('YoutubeFS: getdir ' + path)
        -errno.ENOSYS

    def mythread ( self ):
        logging.debug('YoutubeFS: mythread')
        -errno.ENOSYS

    def chmod ( self, path, mode ):
        logging.debug('YoutubeFS: chmod ' + path + ' ' + mode)
        -errno.ENOSYS

    def chown ( self, path, uid, gid ):
        logging.debug('YoutubeFS: chown ' + path + \
            + ' ' + uid + ' ' + gid)
        -errno.ENOSYS

    def fsync ( self, path, isFsyncFile ):
        print '*** fsync', path, isFsyncFile
        logging.debug('YoutubeFS: fsync' + path)
        -errno.ENOSYS

    def link ( self, targetPath, linkPath ):
        print '*** link', targetPath, linkPath
        logging.debug('YoutubeFS: link ' + targetPath + \
            ' ' + linkPath)
        -errno.ENOSYS

    def mkdir ( self, path, mode ):
        logging.debug('YoutubeFS: mkdir ' + path + ' ' + 
                mode) 
        -errno.ENOSYS

    def mknod ( self, path, mode, dev ):
        logging.debug('YoutubeFS: mknod ' + path + ' ' +\
                mode + ' ' + dev)
        -errno.ENOSYS

    def open ( self, path, flags ):
        logging.debug('YoutubeFS: open ' + path + ' ' +\
            str(flags()
        -errno.ENOSYS

    def read ( self, path, length, offset ):
        logging.debug('YoutubeFS: read ' + path + ' ' +
            str(length) + ' ' + str(offset))
        -errno.ENOSYS

    def readlink ( self, path ):
        logging.debug('YoutubeFS: readlink ' + path)
        -errno.ENOSYS

    def release ( self, path, flags ):
        logging.debug('YoutubeFS: release ' + path + \
            ' ' + str(flags)) 
        -errno.ENOSYS

    def rename ( self, oldPath, newPath ):
        logging.debug('YoutubeFS: rename ' + oldPath +\
            ' ' + newPath)
        -errno.ENOSYS

    def rmdir ( self, path ):
        logging.debug('YoutubeFS: rmdir ' + path)
        -errno.ENOSYS

    def statfs ( self ):
        logging.debug('YoutubeFS: statfs')
        -errno.ENOSYS

    def symlink ( self, targetPath, linkPath ):
        logging.debug('YoutubeFS: symlink ' + targetPath +\
            ' ' + linkPath)
        -errno.ENOSYS

    def truncate ( self, path, size ):
        logging.debug('YoutubeFS: truncate ' + path + \
            ' ' + str(size))
        -errno.ENOSYS

    def unlink ( self, path ):
        logging.debug('YoutubeFS: unlink ' + path)
        -errno.ENOSYS

    def utime ( self, path, times ):
        logging.debug('YoutubeFS: utime ' + path + \
            ' ' + str(times))
        -errno.ENOSYS

    def write ( self, path, buf, offset ):
        logging.debug('YoutubeFS: write ' + path + \
            ' ' + str(buf) + ' ' + str(offset))
        -errno.ENOSYS

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        print sys.argv[0] + " username"
        sys.exit(1)

 
