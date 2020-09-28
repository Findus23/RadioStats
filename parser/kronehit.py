from parser import BaseFetcher
from utils import *

URL = "https://www.kronehit.at/alles-ueber-kronehit/hitsuche/?format=json&channel=1"


class KroneHitFetcher(BaseFetcher):
    def get(self, channel):
        for track in fetch(URL, True)["items"]:
            artist = track["ArtistName"]
            title = track["TrackName"]
            time = time_to_date(string_to_time(track["PlayTime"], seconds=False))
            yield time, artist, title
