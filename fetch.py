from datetime import datetime, timedelta
from time import sleep

import requests

from models import *

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; RadioStats/1.0;)',
}


def careful_fetch(url):
    """
    :rtype: requests.models.Response
    """
    print(url)
    result = None
    tries = 0
    while result is None:
        try:
            req = requests.get(url, headers=headers)
            if "Invalid resource" in req.text:
                raise requests.exceptions.ConnectionError
            return req

        except requests.exceptions.ConnectionError:
            print("404")
            tries += 1
            if tries >= 3:
                raise Exception("too many retries")
            sleep(1)
            pass


def detect_show(artist, title):
    return "Ö3" in artist or "LiveStream" in title or "Radio Tirol" in title \
           or "mein radio" in title.lower() or "SCHOENSTEN OLDIES" in title \
           or "RADIO STEIERMARK" in title or "Radio Burgenland" in title \
           or "FM4 " in title or "Radio Salzburg" in title \
           or "RADIO OÖ" == title or "Radio Wien" in title \
           or (title == "" and artist == "")


def add_entry(time, artist, title):
    print(time, artist, title)
    try:
        song_object = Song.get(artist=artist, title=title)
    except DoesNotExist:
        song_object = Song.create(artist=artist, title=title, show=detect_show(artist, title))

    query = Play.select().where((Play.song == song_object) & (Play.channel == channel) &
                                (Play.time.between(time - timedelta(minutes=20), time + timedelta(minutes=20))))
    if query.exists():
        print("has already been added")
    else:
        try:
            Play.create(song=song_object, channel=channel, time=time)
            raise IntegrityError
        except IntegrityError as error:
            print(error)


for channel in Channel.select():
    if channel.has_data:
        r = careful_fetch(channel.streamurl + "played.html?type=json")
        print(r.text)
        for song in r.json():
            time = datetime.fromtimestamp(song["playedat"])

            if " - " in song["title"]:
                if channel.shortname == "oe3" or channel.shortname=="fm4":
                    artist, title = song["title"].split(" - ")[:2]
                else:
                    title, artist = song["title"].split(" - ")[:2]  # non oe3 channels are the other way round
            else:
                artist = ""
                title = song["title"]
            if channel.shortname == "fm4" and "|" in title:
                title = title.split("|")[0]

            add_entry(time, artist, title)
