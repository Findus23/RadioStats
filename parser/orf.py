from parser import BaseFetcher
from utils import *


class OrfFetcher(BaseFetcher):
    def get(self, channel):
        r = careful_fetch(f"https://audioapi.orf.at/{channel.shortname}/json/4.0/live")
        r.raise_for_status()
        for song in r.json()[0]["items"]:
            time = datetime.fromtimestamp(song["start"] / 1000)
            try:
                artist = song["interpreter"]
                title = song["title"]
            except KeyError:
                print("not a song")
                continue
            yield (time, artist, title)
