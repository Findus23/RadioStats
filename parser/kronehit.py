from utils import *

URL = "https://www.kronehit.at/alles-ueber-kronehit/hitsuche/?format=json&channel=1"


def get(channel):
    for track in fetch(URL, True)["items"]:
        artist = track["ArtistName"]
        title = track["TrackName"]
        print(track["PlayTime"])
        time = time_to_date(string_to_time(track["PlayTime"]))
        print(string_to_time(track["PlayTime"]))
        yield time, artist, title
