"""
This file contains all the models for the awx proxy
"""
import json
import requests
import time


class PlexDownloads:
    """
    This class handles the loading of raw json, and returns the plex version for download
    """

    def __init__(self):
        self.json = None

    def get_latest_version_from_plex(self):
        plex_download_url = "https://plex.tv/api/downloads/5.json?channel=plexpass&cb={}".format(int(time.time()))
        r = requests.get(plex_download_url)
        self.json = json.loads(r.text)

    def get_latest_version(self):
        return self.json['computer']['Linux']['version']
