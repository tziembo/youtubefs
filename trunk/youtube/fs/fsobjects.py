#!/usr/bin/env python

__author__      = "Vishal Patil"
__copyright__   = "Copyright 2007 - 2008, Vishal Patil"
__license__     = "MIT"

from fuse import Stat
from fuse import Direntry
from youtube.api.protocol import YoutubeVideo
from youtube.api.protocol import YoutubePlaylist
from youtube.api.protocol import YoutubeUser
import time
import os

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

    def __str__(self):
        tuple = (self.st_mode, self.st_ino, self.st_dev, \
                self.st_nlink, self.st_uid, self.st_gid,\
                self.st_size, self.st_atime, self.st_mtime, \
                self.st_ctime)        
        return str(tuple) 

class YoutubeFSInode:
    def __init__(self,path,id,ctime,mtime):
        self.path           =   path
        self.stat           =   YoutubeFUSEStat()
        self.stat.st_ino    =   id 
        self.stat.st_ctime  =   ctime 
        self.stat.st_mtime  =   mtime
        self.data           = ""
        self.children       = []        

"""
    A very basic inode cache, this data structure would be 
    modified later for speedy access as well as to decrease
    the memory footprint.
"""
class YoutubeFSInodeCache:
    cache = {}    

    def addInode(self,inode):
        self.cache[inode.path] = inode

    def getInode(self,path):
        if self.cache.has_key(id):
            return self.cache[id]

        return None 

    def __str__(self):
        str = ""
        for k,v in self.cache.iteritems():
            str = str + ("%s\n" % k)       
        return str            
