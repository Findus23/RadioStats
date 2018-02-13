from utils import *


def get(channel):
    r = careful_fetch(channel.streamurl + "played.html?type=json")
    print(r.text)
    for song in r.json():
        time = datetime.fromtimestamp(song["playedat"])

        if " - " in song["title"]:
            if channel.shortname == "oe3" or channel.shortname == "fm4":
                artist, title = song["title"].split(" - ")[:2]
            else:
                title, artist = song["title"].split(" - ")[:2]  # non oe3 channels are the other way round
        else:
            artist = ""
            title = song["title"]
        if channel.shortname == "fm4" and "|" in title:
            title = title.split("|")[0]

        yield (time, artist, title)
