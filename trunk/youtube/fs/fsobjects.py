#!/usr/bin/env python

__author__      = "Vishal Patil"
__copyright__   = "Copyright 2007 - 2008, Vishal Patil"
__license__     = "MIT"

import youtube.api.protocol.YoutubeVideo
import youtube.api.protocol.YoutubePlaylist
import youtube.api.protocol.YoutubeUser
import time
import os

class YoutubeFSInode:
    def __init__(self,id,ctime,mtime):
       self.id      = id 
       self.ctime   = ctime
       self.mtime   = mtime
       self.atime   = int(time.time()) 

class YoutubeFSFileInode(YoutubeFS_Inode):
    def __init__(self,id,ctime,mtime\
            title,url,type):
       YoutubeFS_Inode.__init__(id,ctime,\
                mtime)
       self.title   = title
       self.url     = url
       self.type    = type  

class YoutubeFSDirInode(YoutubeFS_Inode):
    def __init__(self,id,ctime,mtime\
            title,url,type):
       YoutubeFS_Inode.__init__(id,ctime,\
                mtime)
       self.title   = title
       self.url     = url
       self.type    = type  


"""
    A very basic inode cache, this data structure would be 
    modified later for speedy access as well as to decrease
    the memory footprint.
"""
class YoutubeFSInodeCache:
    cache = {}    

    def addInode(self,inode):
        self.cache[inode.id] = inode

    def getInode(self,id):
        if self.cache.has_key(id):
            return self.cache[id]

        return None 


