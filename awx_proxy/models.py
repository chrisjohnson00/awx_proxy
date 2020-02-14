"""
PlexDownloads is the class to rule all the plexes functionalities
"""
import json
import requests
import time


class PlexDownloads:
    """
    PlexDownloads handles the loading of raw json, and returns the plex version for download.
    """

    def __init__(self):
        """Constructor for PlexDownloads."""
        self.json = None

    def get_latest_version_from_plex(self):
        """Fetches a json payload from plex's site."""
        plex_download_url = "https://plex.tv/api/downloads/5.json?channel=plexpass&cb={}".format(int(time.time()))
        r = requests.get(plex_download_url)
        self.json = json.loads(r.text)

    def get_latest_version(self):
        """Returns the latest version from the json payload."""
        return self.json['computer']['Linux']['version']
