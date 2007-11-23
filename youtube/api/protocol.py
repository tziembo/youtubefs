#!/usr/bin/env python

import logging
import urllib2
import sys
import youtube.api

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
 
    def getPlaylists(self):
        url = youtube.api.PLAYLISTS_URI % (self.__username__)
        logging.debug(url)

    def getFavourities(self):
        pass

    def getSubscriptions(self):
        pass

    def getProfile(self):
        pass

    def getContacts(self):
        pass

 
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print sys.argv[0] + " username "
        sys.exit(1)

    youtubeUser = YoutubeUser(sys.argv[1])
    youtubeUser.getPlaylists()
 
