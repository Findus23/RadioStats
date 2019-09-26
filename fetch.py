from datetime import timedelta

import sentry_sdk
import config
from models import *
from parser import kronehit, aas, orf, ara

if config.sentryDSN:
    client = sentry_sdk.init(dsn=config.sentryDSN)

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; RadioStats/1.0;)',
}


def detect_show(artist, title):
    return "Ö3" in artist or "LiveStream" in title or "Radio Tirol" in title \
           or "mein radio" in title.lower() or "SCHOENSTEN OLDIES" in title \
           or "RADIO STEIERMARK" in title or "Radio Burgenland" in title \
           or "FM4 " in title or "Radio Salzburg" in title \
           or "RADIO OÖ" == title or "Radio Wien" in title \
           or (title == "" and artist == "")


def add_entry(time, artist, title):
    print(time, artist, title)
    if artist.isupper():
        artist = artist.title()
    if title.isupper():
        title = title.title()
    title = title.replace("+", " ")
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
        if channel.shortname == "kht":
            pars = kronehit
        elif channel.shortname == "886":
            pars = aas
        elif channel.shortname == "ara":
            pars = ara
        elif channel.shortname == "eng":
            continue
        elif channel.shortname == "all":
            continue
        else:
            pars = orf

        for time, artist, title in pars.get(channel):
            add_entry(time, artist, title)
