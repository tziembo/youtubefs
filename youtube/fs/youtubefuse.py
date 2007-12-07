#!/usr/bin/env python
__author__      = "Vishal Patil"
__copyright__   = "Copyright 2007 - 2008, Vishal Patil"
__license__     = "MIT"

import logging
import os, sys
import fcntl
import stat
import time
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse
from youtube.api.protocol import YoutubeUser
from youtube.api.protocol import YoutubeVideo
from youtube.api.protocol import YoutubePlaylist
from youtube.api.protocol import YoutubeProfile
from youtube.api import gdataTime2UnixTime
from youtube.fs.fsobjects import YoutubeStat
from youtube.fs.fsobjects import YoutubeFSInodeCache
from youtube.fs.fsobjects import YoutubeFSInode

class YoutubeFUSE(Fuse):
    def __init__(self, *args, **kw):
        Fuse.__init__(self, *args, **kw)
        self.root = '/'
        self.youtubeUser = None
        self.inodeCache  =  YoutubeFSInodeCache()
        logging.debug("YoutubeFUSE init complete")

    def open(self,path,flags):
        logging.debug("YoutubeFUSE open called")
        file = self.YoutubeFUSEFile(path,0,0)
        return file 

    def getattr(self, path):
        logging.debug("YoutubeFUSE getattr for " + path)
        inode = self.inodeCache.getInode(path)
        logging.debug("YoutubeFUSE new getattr for %s is %s",\
                inode.path,str(inode.stat))
        return inode.stat 

    def readlink(self, path):
        logging.debug("YoutubeFUSE readlink " + path)
        return os.readlink("." + path)

    def readdir(self, path, offset):
        logging.debug("YoutubeFUSE readdir " + path + \
                + " " + str(offset))

        dirInode = self.inodeCache.getInode(self.path)
        for entry in dirInode.children:
            log.debug("YoutubeFUSE readdir returning subdir " + \
                        entry)
            yield fuse.fuseDirentry(entry.path.strip('/').encode('ascii'))

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
        self.createfs()
        os.chdir(self.root)

    def __addRootInode(self):
            #
            # Added the root directory inode
            #
            mode = stat.S_IFDIR | 0755
            rootDirInode = YoutubeFSInode('/',mode,0,\
                long(time.time()),long(time.time())) 
            self.inodeCache.addInode(rootDirInode)

    def __addProfileInode(self):
            #
            # Add the profile file
            #
            profile = self.youtubeUser.getProfile()
            mode = stat.S_IFREG | 0444
            profileInode = YoutubeFSInode('/profile',mode,\
                    0,profile.ctime,profile.mtime)
            profileInode.ctime  = profile.ctime
            profileInode.mtime  = profile.mtime
            profileInode.data   = profile.getData()
            self.inodeCache.addInode(profileInode) 
            rootDirInode = self.inodeCache.getInode('/')
            rootDirInode.addChildInode(profileInode)

    def __addFavouritesInode(self):
            #
            # Get the favourite videos
            # 
            favourities = self.youtubeUser.getFavourities()
            mode = stat.S_IFDIR | 0755
            favouritesInode = YoutubeFSInode('/favourites',mode,\
                    0,favourities.ctime,favourities.mtime)
            self.inodeCache.addInode(favouritesInode) 
            rootDirInode = self.inodeCache.getInode('/')
            rootDirInode.addChildInode(favouritesInode)
        
            for video in favourities.getVideos():
                mode = stat.S_IFREG | 0444
                path = ("/favourites/%s") % video.title
                videoInode =  YoutubeFSInode(path,mode,\
                            video.id,video.ctime,video.mtime)
                videoInode.data = video.getContents()
                self.inodeCache.addInode(videoInode) 
                favouritesInode.addChildInode(videoInode)

    def __addPlaylistInodes(self):
        pass
            
    def createfs(self):
        try:
            logging.debug("YoutubeFUSE createfs")
            self.youtubeUser = YoutubeUser(self.username)

            self.__addRootInode()
            self.__addProfileInode()     
            self.__addFavouritesInode()
            self.__addPlaylistInodes()       
            
            print str(self.inodeCache) 
        except Exception,inst:
            logging.debug("YoutubeFUSE createfs exception : " + str(inst))

    def main(self, *a, **kw):
        return Fuse.main(self, *a, **kw)



