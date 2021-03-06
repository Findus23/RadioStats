from parser import BaseFetcher
from utils import *

URL = "http://www.arabella.at/live-feed/ajax.php?station=zenon-rp-wien"


class ArabellaFetcher(BaseFetcher):
    def get(self, channel):
        response = fetch(URL, True)
        if response:
            for track in response["songs"]:
                artist = track["artist"]
                title = track["title"]
                dt = track["start_date_time"]
                time = datetime(year=int(dt["year"]), month=int(dt["month"]), day=int(dt["day"]),
                                hour=int(dt["hours"]), minute=int(dt["minutes"]), second=int(dt["seconds"]))
                yield time, artist, title
