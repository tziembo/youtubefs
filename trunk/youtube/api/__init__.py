#!/usr/bin/env python

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='youtube.api.log',
                    filemode='w')

PLAYLISTS_URI       = "http://gdata.youtube.com/feeds/" +\
                        "projection/users/%s/playlists"

PROFILE_URI         = "http://gdata.youtube.com/feeds/"+\
                        "projection/users/%s" 

CONTACTS_URI        = "http://gdata.youtube.com/feeds/" +\
                        "projection/users/%s/contacts" 

SUBSCRIPTIONS_URI   = "http://gdata.youtube.com/feeds/" +\
                        "projection/users/%s/subscriptions"
