from utils import *
from sentry_sdk import capture_exception
URL = "https://meta.radio886.at/886/0"


def get(channel):
    data = fetch(URL, True)
    if "data" not in data:
        capture_exception(Exception("886 didn't return any data."))
        return []
    for track in fetch(URL, True)["data"]:
        artist = track["name"]
        title = track["title"]
        try:
            time = time_to_date(string_to_time(track["scheduled_time"]))
            yield time, artist, title
        except ValueError as e:  # in case time is 24:02:31 or similar
            print(e)
