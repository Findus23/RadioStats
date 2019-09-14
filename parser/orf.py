from utils import *


def get(channel):
    r = careful_fetch(channel.streamurl + "played.html?type=json")
    print(r.text)
    for song in r.json():
        time = datetime.fromtimestamp(song["playedat"])

        if " - " in song["title"]:
            # for whatever crazy reason only half of the channels are the other way round
            if channel.shortname in ["oe3", "fm4", "noe", "wie", "stm"]:
                artist, title = song["title"].split(" - ")[:2]
            else:
                title, artist = song["title"].split(" - ")[:2]
        else:
            artist = ""
            title = song["title"]
        if channel.shortname == "fm4" and "|" in title:
            title = title.split("|")[0]

        yield (time, artist, title)
