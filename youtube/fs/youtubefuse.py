#!/usr/bin/env python
__author__      = "Vishal Patil"
__copyright__   = "Copyright 2007 - 2008, Vishal Patil"
__license__     = "MIT"

import logging
import os, sys
import fcntl
import stat
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse
from fuse import Stat
from youtube.api.protocol import YoutubeUser
from youtube.api.protocol import YoutubeVideo
from youtube.api.protocol import YoutubePlaylist

if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

def flag2mode(flags):
    md = {os.O_RDONLY: 'r', os.O_WRONLY: 'w', os.O_RDWR: 'w+'}
    m = md[flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR)]

    if flags | os.O_APPEND:
        m = m.replace('w', 'a', 1)

    return m

class YoutubeStat(Stat):
    def __init__(self):
        self.st_ino     = ""
        self.st_mode    = 0
        self.st_dev     = ""
        self.st_nlink   = 0
        self.st_rdev    = ""
        self.st_size    = 0
        self.st_blksize = 0
        self.st_blocks  = 0
        self.st_uid     = 0 
        self.st_gid     = 0 
        self.st_atime   = 0
        self.st_mtime   = 0
        self.st_ctime   = 0

    def copy(self,source):
        self.st_ino     = source.st_ino 
        self.st_mode    = source.st_mode 
        self.st_dev     = source.st_dev 
        self.st_nlink   = source.st_nlink
        self.st_rdev    = source.st_rdev
        self.st_size    = source.st_size
        self.st_blksize = source.st_blksize
        self.st_blocks  = source.st_blocks
        self.st_uid     = source.st_uid
        self.st_gid     = source.st_gid
        self.st_atime   = source.st_atime
        self.st_mtime   = source.st_mtime
        self.st_ctime   = source.st_ctime

class YoutubeFUSE(Fuse):
    def __init__(self, *args, **kw):
        Fuse.__init__(self, *args, **kw)
        self.root = '/'
        self.username = ""
        logging.debug("YoutubeFUSE init complete")

    def getattr(self, path):
        attr = os.lstat("." + path)
        logging.debug("YoutubeFUSE getattr " + path + " " +\
                            str(attr))

        if (path == "/"):
            mode = stat.S_IFDIR | 0755 
        else:
            mode = stat.S_IFREG | 0644
      
        logging.debug("YoutubeFUSE old getattr " + str(attr) +\
            " " + str(type(attr)))
        try:
            myattr  = YoutubeStat()
            myattr.copy(attr)
            myattr.st_mode = mode
        except Exception, e:
            logging.debug("Problem setting the attribute " +\
                str(e))
        logging.debug("YoutubeFUSE new getattr " + str(myattr))
        return myattr

    def readlink(self, path):
        logging.debug("YoutubeFUSE readlink " + path)
        return os.readlink("." + path)

    def readdir(self, path, offset):
        logging.debug("YoutubeFUSE readdir " + path)
        for e in os.listdir("." + path):
            logging.debug("YoutubeFUSE direntry " + e)   
            yield fuse.Direntry(e)

    def unlink(self, path):
        logging.debug("YoutubeFUSE unlink " + path)
        os.unlink("." + path)

    def rmdir(self, path):
        logging.debug("YoutubeFUSE rmdir " + path)
        os.rmdir("." + path)

    def symlink(self, path, path1):
        logging.debug("YoutubeFUSE symlink " + path\
            + " " + path1)
        os.symlink(path, "." + path1)

    def rename(self, path, path1):
        logging.debug("YoutubeFUSE rename " + path\
            + " " + path1)
        os.rename("." + path, "." + path1)

    def link(self, path, path1):
        logging.debug("YoutubeFUSE link " + path\
            + " " + path1)
        os.link("." + path, "." + path1)

    def chmod(self, path, mode):
        logging.debug("YoutubeFUSE chmod " + path
            + " " + str(mode))
        os.chmod("." + path, mode)

    def chown(self, path, user, group):
        logging.debug("YoutubeFUSE chown " + path\
            + " " + user + " " + group)
        os.chown("." + path, user, group)

    def truncate(self, path, len):
        logging.debug("YoutubeFUSE truncate " +\
            path + " " + str(len))
        f = open("." + path, "a")
        f.truncate(len)
        f.close()

    def mknod(self, path, mode, dev):
        logging.debug("YoutubeFUSE mknode" +\
        path + " " + str(mode) + " " + str(dev))
        os.mknod("." + path, mode, dev)

    def mkdir(self, path, mode):
        logging.debug("YoutubeFUSE mkdir " +\
            path + " " + str(mode)) 
        os.mkdir("." + path, mode)

    def utime(self, path, times):
        logging.debug("YoutubeFUSE utime " + path +\
            " " + str(times))
        os.utime("." + path, times)

    def access(self, path, mode):
        logging.debug("YoutubeFUSE access " + path +\
            " " + str(mode))
        if not os.access("." + path, mode):
            return -EACCES

    def statfs(self):
        """
        Should return an object with statvfs attributes (f_bsize, f_frsize...).
        Eg., the return value of os.statvfs() is such a thing (since py 2.2).
        If you are not reusing an existing statvfs object, start with
        fuse.StatVFS(), and define the attributes.

        To provide usable information (ie., you want sensible df(1)
        output, you are suggested to specify the following attributes:

            - f_bsize - preferred size of file blocks, in bytes
            - f_frsize - fundamental size of file blcoks, in bytes
                [if you have no idea, use the same as blocksize]
            - f_blocks - total number of blocks in the filesystem
            - f_bfree - number of free blocks
            - f_files - total number of file inodes
            - f_ffree - nunber of free file inodes
        """
        logging.debug("YoutubeFUSE statfs")
        return os.statvfs(".")

    def fsinit(self):
        logging.debug("YoutubeFUSE fsinit " + self.username)
        os.chdir(self.root)

    class YoutubeFUSEFile(object):

        def __init__(self, path, flags, *mode):
            self.file = os.fdopen(os.open("." + path, flags, *mode),
                                  flag2mode(flags))
            self.fd = self.file.fileno()

        def read(self, length, offset):
            self.file.seek(offset)
            return self.file.read(length)

        def write(self, buf, offset):
            self.file.seek(offset)
            self.file.write(buf)
            return len(buf)

        def release(self, flags):
            self.file.close()

        def _fflush(self):
            if 'w' in self.file.mode or 'a' in self.file.mode:
                self.file.flush()

        def fsync(self, isfsyncfile):
            self._fflush()
            if isfsyncfile and hasattr(os, 'fdatasync'):
                os.fdatasync(self.fd)
            else:
                os.fsync(self.fd)

        def flush(self):
            self._fflush()
            os.close(os.dup(self.fd))

        def fgetattr(self):
            return os.fstat(self.fd)

        def ftruncate(self, len):
            self.file.truncate(len)

        def lock(self, cmd, owner, **kw):
            # The code here is much rather just a demonstration of the locking
            # API than something which actually was seen to be useful.

            # Advisory file locking is pretty messy in Unix, and the Python
            # interface to this doesn't make it better.
            # We can't do fcntl(2)/F_GETLK from Python in a platfrom independent
            # way. The following implementation *might* work under Linux. 
            #
            # if cmd == fcntl.F_GETLK:
            #     import struct
            # 
            #     lockdata = struct.pack('hhQQi', kw['l_type'], os.SEEK_SET,
            #                            kw['l_start'], kw['l_len'], kw['l_pid'])
            #     ld2 = fcntl.fcntl(self.fd, fcntl.F_GETLK, lockdata)
            #     flockfields = ('l_type', 'l_whence', 'l_start', 'l_len', 'l_pid')
            #     uld2 = struct.unpack('hhQQi', ld2)
            #     res = {}
            #     for i in xrange(len(uld2)):
            #          res[flockfields[i]] = uld2[i]
            #  
            #     return fuse.Flock(**res)

            # Convert fcntl-ish lock parameters to Python's weird
            # lockf(3)/flock(2) medley locking API...
            op = { fcntl.F_UNLCK : fcntl.LOCK_UN,
                   fcntl.F_RDLCK : fcntl.LOCK_SH,
                   fcntl.F_WRLCK : fcntl.LOCK_EX }[kw['l_type']]
            if cmd == fcntl.F_GETLK:
                return -EOPNOTSUPP
            elif cmd == fcntl.F_SETLK:
                if op != fcntl.LOCK_UN:
                    op |= fcntl.LOCK_NB
            elif cmd == fcntl.F_SETLKW:
                pass
            else:
                return -EINVAL
            fcntl.lockf(self.fd, op, kw['l_start'], kw['l_len'])


    def main(self, *a, **kw):
        self.file_class = self.YoutubeFUSEFile
        return Fuse.main(self, *a, **kw)



