#!/usr/bin/env python
__author__      = "Vishal Patil"
__copyright__   = "Copyright 2007 - 2008, Vishal Patil"
__license__     = "MIT"

import re
import logging
import datetime
import time
from time import mktime 

logging.basicConfig(level=logging.CRITICAL,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='youtube.api.log',
                    filemode='w')

PLAYLISTS_URI       = "http://gdata.youtube.com/feeds/" +\
                        "api/users/%s/playlists"

PLAYLISTS_URI_ERROR = "Unable to get the playlists for %s"

PLAYLIST_VIDEOS_URI = "http://gdata.youtube.com/feeds/api/" +\
                        "playlists/%s"
PLAYLIST_VIDEOS_ERROR = "Unable to get the videos for %s"

PROFILE_URI         = "http://gdata.youtube.com/feeds/"+\
                        "api/users/%s"
 
PROFILE_URI_ERROR = "Unable to access the profile for %s"

FAVOURITES_URI   = \
    "http://gdata.youtube.com/feeds/api/users/%s/favorites"

CONTACTS_URI        = "http://gdata.youtube.com/feeds/" +\
                        "api/users/%s/contacts" 

SUBSCRIPTIONS_URI   = "http://gdata.youtube.com/feeds/" +\
                        "api/users/%s/subscriptions"

META_TAG    = "<META HTTP-EQUIV=\"Refresh\" CONTENT=\"1 URL=%s\">"

def gdataTime2UnixTime(gdate):
    isodate = re.compile('[.:T-]').split(gdate)
    year        = int(isodate[0])
    month       = int(isodate[1])
    day         = int(isodate[2])
    hour        = int(isodate[3])
    minute      = int(isodate[4])
    seconds     = int(isodate[5])

    t = (datetime.datetime(year,month,day,\
                hour,minute,seconds))
    logging.debug("gdataTime2UnixTime: " + str(t))
    return long(mktime(t.timetuple())+1e-6*t.microsecond)

