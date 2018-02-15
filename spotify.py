from time import sleep

import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

from config import spotify
from models import *

crm = SpotifyClientCredentials(**spotify)
sp = spotipy.Spotify(client_credentials_manager=crm)

if len(sys.argv) >1:
    limit=sys.argv[1]

for song in Song.select().where((Song.spotify_data.is_null()) & (Song.show == 0)).limit(50):
    print(song.title)
    if song.artist.isupper():
        song.artist = song.artist.title()
    if song.title.isupper():
        song.title = song.title.title()

    sleep(0.1)
    results = sp.search(q='title:' + song.title + ' artist:' + song.artist, type='track', limit=1)
    if len(results["tracks"]["items"]) == 0:
        song.spotify_data = False
    else:
        track = results["tracks"]["items"][0]
        song.spotify_url = track["external_urls"]["spotify"]
        song.preview_url = track["preview_url"]
        images = track["album"]["images"]
        song.image_large = images[0]["url"]
        song.image_small = images[-1]["url"]
        song.spotify_data = True

        # print(song.title)
        # print(track["name"])
        # print(song.artist)
        # print(", ".join([a["name"] for a in track["artists"]]))

    song.save()
