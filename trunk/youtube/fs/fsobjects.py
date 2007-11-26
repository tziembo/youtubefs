#!/usr/bin/env python

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

class YoutubeFSInodeCache:
    pass


