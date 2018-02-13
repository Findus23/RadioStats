from utils import *

URL = "http://www.arabella.at/live-feed/ajax.php?station=zenon-rp-wien"


def get(channel):
    for track in fetch(URL, True)["songs"]:
        artist = track["artist"]
        title = track["title"]
        dt = track["start_date_time"]
        time = datetime(year=int(dt["year"]), month=int(dt["month"]), day=int(dt["day"]),
                        hour=int(dt["hours"]), minute=int(dt["minutes"]), second=int(dt["seconds"]))
        yield time, artist, title
