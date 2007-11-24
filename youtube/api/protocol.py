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
        splits           = self.id.split('/')
        self.playlist_id = splits[len(splits) - 1]
   
    def getVideos(self):
        videos = []
        url    = youtube.api.PLAYLIST_VIDEOS_URI\
            % self.playlist_id   
        logging.debug(url)

        try:
            urlObj = urllib2.urlopen(url)
            data   = urlObj.read()
        except:
            logging.critical("Unable to open " + url)
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

                videos.append(video)

                mediaGroup      = (entry.getElementsByTagName('media:group')[0])
                mediaContent    = (mediaGroup.getElementsByTagName('media:content'))

                if mediaContent:
                    print mediaContent[0].toxml()

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
        splits           = self.id.split('/')
        self.video_id = splits[len(splits) - 1]

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
    playlists = youtubeUser.getPlaylists()
    for playlist in playlists:
        playlist.getVideos()

 
