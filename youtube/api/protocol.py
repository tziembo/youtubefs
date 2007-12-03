#!/usr/bin/env python

__author__      = "Vishal Patil"
__copyright__   = "Copyright 2007 - 2008, Vishal Patil"
__license__     = "MIT"

import logging
import urllib2
import sys
import youtube.api
import xml.dom.minidom

class YoutubeProfile:
    def __init__(self):
        self.ctime  =   ""
        self.mtime  =   ""
        self.age    =   "" 
        self.username   =  ""
        self.gender     = ""
        self.location   = "" 

    def __str__(self):
        str =   ("Username   = %s\n" +\
                "Gender     = %s\n" +\
                "Age        = %s\n" +\
                "Location   = %s\n" +\
                "Ctime      = %s\n" +\
                "Mtime      = %s\n") %\
        (self.username,self.gender,self.age,self.location,\
            self.ctime,self.mtime)

        return str

class YoutubePlaylist:
    def __init__(self,id):
        self.id = id
        self.title = ""  
        self.ctime = ""
        self.mtime = ""
        splits           = self.id.split('/')
        self.playlist_id = splits[len(splits) - 1]
        self.url    = youtube.api.PLAYLIST_VIDEOS_URI\
            % self.playlist_id   
   
    def getVideos(self):
        videos = []
        logging.debug(self.url)

        try:
            urlObj = urllib2.urlopen(self.url)
            data   = urlObj.read()
        except:
            logging.critical("Unable to open " + self.url)
            print youtube.api.PLAYLIST_VIDEOS_ERROR % self.playlist_id 

        dom = xml.dom.minidom.parseString(data)
        try:
            for entry in dom.getElementsByTagName('entry'):
                id = (entry.getElementsByTagName('id')[0]).firstChild.data
                video = YoutubeVideo(id)
                logging.debug("Video id: " + video.id)

                video.title =  \
                    (entry.getElementsByTagName('title')[0]).firstChild.data
                logging.debug("Video title: " + video.title)

                video.mtime = \
                    (entry.getElementsByTagName('updated')[0]).firstChild.data
                logging.debug("Video mtime: " + video.mtime)

                mediaGroup      = (entry.getElementsByTagName('media:group')[0])
                mediaContent    = (mediaGroup.getElementsByTagName('media:content'))

                if mediaContent and \
                        mediaContent[0].getAttribute('type') \
                            == "application/x-shockwave-flash":
                    video.url   =  mediaContent[0].getAttribute('url')
                    video.type  =  mediaContent[0].getAttribute('type')
                
                videos.append(video)
        except:
            logging.critical("Invalid video XML format " + \
                        str(sys.exc_info()[0]))
        return videos

class YoutubeVideo:
    def __init__(self,id):
        self.id = id
        self.title = ""  
        self.ctime = ""
        self.mtime = ""
        self.url   = ""
        self.type  = ""
        splits           = self.id.split('/')
        self.video_id = splits[len(splits) - 1]

    def getContents(self):
        content = youtube.api.META_TAG % self.url
        return content        

    def __str__(self):
        str = self.id + "\n" + \
            self.title + "\n" + \
            self.url   
        return str
            

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
        except:
            logging.critical("Unable to open " + url)

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

        return playlists        

    """
        Returns a YoutubePlaylist object containing all
        of the user's favourite videos.
    """
    def getFavourities(self):
        videos = []
        url    = youtube.api.FAVOURITES_URI\
            % self.__username__
        favourities = YoutubePlaylist(url) 
        favourities.url = url
        return favourities 
    
    def getSubscriptions(self):
        pass

    def getProfile(self):
        url = youtube.api.PROFILE_URI % (self.__username__)
        logging.debug(url)

        try:
            urlObj = urllib2.urlopen(url)
            data   = urlObj.read()
        except:
            logging.critical("Unable to get profile for " + 
                self.__username__)
            print youtube.api.PROFILE_URI_ERROR % self.__username__ 
            sys.exit(1) 

        profile = YoutubeProfile()
        dom = xml.dom.minidom.parseString(data)
        logging.debug(data)
        try:
           for entry in dom.getElementsByTagName('entry'):
               profile.ctime = \
                   (entry.getElementsByTagName('published')[0]).firstChild.data
               logging.debug("Profile ctime: " + pl.ctime)

               profile.mtime = \
                   (entry.getElementsByTagName('updated')[0]).firstChild.data
               logging.debug("Profile mtime: " + pl.mtime)
               
               profile.age    =   (entry.getElementsByTagName('yt:age')[0]).firstChild.data 
               profile.username   = (entry.getElementsByTagName('yt:username')[0]).firstChild.data  
               profile.gender     = (entry.getElementsByTagName('yt:gender')[0]).firstChild.data 
               profile.location   = (entry.getElementsByTagName('yt:location')[0]).firstChild.data  
               logging.debug(("Profile: %s\n" % (profile)));
        except:            
           logging.critical("Invalid playlist XML format " + \
                       str(sys.exc_info()[0]))
        return profile

    def getContacts(self):
        pass

 
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print sys.argv[0] + " username "
        sys.exit(1)

    youtubeUser = YoutubeUser(sys.argv[1])
    youtubeUser.getProfile()
    favourities = youtubeUser.getFavourities()
    for video in favourities:
        print video

    playlists = youtubeUser.getPlaylists()
    for playlist in playlists:
        playlist.getVideos()

 
