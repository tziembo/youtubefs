#!/usr/bin/env python

import urllib2

class YoutubePlaylist:
    def __init__(self,id):
        self.__id__ = id    

class YoutubeVideo:
    def __init__(self,videoURL,playlistId):
        self.__videoURL__   = videoURL
        self.__playlistID__ = playlistId

class YoutubeUser:
    def __init__(self,username):
        self.__username__ = username

    def getPlaylist(self):
        pass

    def getFavourities(self):
        pass

    def getSubscriptions(self):
        pass

    def getProfile(self):
        pass

    def getContacts(self):
        pass

 

