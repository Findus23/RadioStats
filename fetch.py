from datetime import datetime, timedelta
from time import sleep

import requests
from bs4 import BeautifulSoup

from models import *

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; RadioStats/1.0;)',
}


def careful_fetch(url):
    """
    :rtype: requests.models.Response
    """
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
           or "RADIO STEIERMARK" in artist or "Radio Burgenland" in artist


def time_to_date(time):
    """

    :rtype: datetime.datetime
    :type time: datetime.time
    """
    time_hour = time.hour
    day = datetime.now()
    current_hour = day.hour
    if 0 <= current_hour <= 3 and 22 <= time_hour <= 24:
        day = datetime.today() - timedelta(days=1)
    return datetime.combine(day.date(), time)


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
        Play.create(song=song_object, channel=channel, time=time)


for channel in Channel.select():
    if channel.supports_json:
        r = careful_fetch(channel.streamurl + "played.html?type=json")
        print(r.text)
        for song in r.json():
            time = datetime.fromtimestamp(song["playedat"])
            artist, title = song["title"].split(" - ")

            add_entry(time, artist, title)
    else:
        # if channel.shortname != "noe":
        #     continue
        print(channel.streamurl + "played.html")
        r = careful_fetch(channel.streamurl + "played.html")
        soup = BeautifulSoup(r.text.encode('latin1').decode('utf8'), 'html.parser')
        table = soup.find_all("table")[2]
        for b in table("b"):
            b.extract()
        for tr in table.find_all("tr")[1:]:
            tds = tr.find_all("td")
            timestring = tds[0].get_text()
            description = tds[1].get_text()
            if " - " in description:
                print(description)
                artist, title = description.split(" - ")[:2]
            else:
                artist = ""
                title = description
            if channel.shortname == "fm4" and "|" in title:
                title = title.split("|")[0]

            time = time_to_date(datetime.strptime(timestring, "%H:%M:%S").time())
            add_entry(time, artist, title)
