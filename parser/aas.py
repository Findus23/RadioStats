from utils import *

URL = "https://meta.radio886.at/886/0"


def get(channel):
    for track in fetch(URL, True)["data"]:
        artist = track["name"]
        title = track["title"]
        time = time_to_date(string_to_time(track["scheduled_time"]))
        yield time, artist, title
