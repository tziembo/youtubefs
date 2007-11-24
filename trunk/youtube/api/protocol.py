#!/usr/bin/env python

import logging
import urllib2
import sys
import youtube.api
import xml.dom.minidom


class YoutubePlaylist:
    def __init__(self,id):
        self.id = id
        self.title = ""  
        self.ctime = ""
        self.mtime = ""

class YoutubeVideo:
    def __init__(self,videoURL,playlistId):
        self.__videoURL__   = videoURL
        self.__playlistID__ = playlistId

class YoutubeUser:
    def __init__(self,username):
        self.__username__ = username

    def getPlaylists(self):
        
        playlists = []
        url = youtube.api.PLAYLISTS_URI % (self.__username__)
        logging.debug(url)

        try:
            urlObj = urllib2.urlopen(url)
            data   = urlObj.read()
            logging.debug(data)
        except:
            logging.critical("Unable to open " + url)
            print youtube.api.PLAYLISTS_URI_ERROR % self.__username__ 

        dom = xml.dom.minidom.parseString(data)
        try:
            for entry in dom.getElementsByTagName('entry'):
                id = (entry.getElementsByTagName('id')[0]).firstChild.data
                pl = YoutubePlaylist(id)
                logging.debug("Playlist id: " + pl.id)

                pl.title =  \
                    (entry.getElementsByTagName('title')[0]).firstChild.data
                logging.debug("Playlist title: " + pl.title)

                pl.ctime = \
                    (entry.getElementsByTagName('published')[0]).firstChild.data
                logging.debug("Playlist ctime: " + pl.ctime)

                pl.mtime = \
                    (entry.getElementsByTagName('updated')[0]).firstChild.data
                logging.debug("Playlist mtime: " + pl.mtime)
                playlists.append(pl)
        except:            
            logging.critical("Invalid playlist XML format " + \
                        str(sys.exc_info()[0]))
            print "Invalid playlist XML format" + url

    def getFavourities(self):
        pass

    def getSubscriptions(self):
        pass

    def getProfile(self):
        url = youtube.api.PROFILE_URI % (self.__username__)
        logging.debug(url)

        try:
            urlObj = urllib2.urlopen(url)
            data   = urlObj.read()
            logging.debug(data)
        except:
            logging.critical("Unable to get profile for " + 
                self.__username__)
            print youtube.api.PROFILE_URI_ERROR % self.__username__ 
            sys.exit(1) 

    def getContacts(self):
        pass

 
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print sys.argv[0] + " username "
        sys.exit(1)

    youtubeUser = YoutubeUser(sys.argv[1])
    youtubeUser.getProfile()
    youtubeUser.getPlaylists()
 
