#!/usr/bin/env python

import sys
from youtube.api.protocol import YoutubeVideo
from youtube.api.protocol import YoutubePlaylist
from youtube.api.protocol import YoutubeUser

class YoutubeFS:
    """
    
    """
    def __init__(self,username):
        self.__youtubeuser__ = YoutubeUser(username)


if __name__ == "__main__":
    if (len(sys.argv) == 2):
        print sys.argv[0] + " username"
        sys.exit(1)

 
