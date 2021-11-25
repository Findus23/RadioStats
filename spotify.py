import json
import re
import sys
from time import sleep

import sentry_sdk
import spotipy
from redis import Redis
from spotipy import CacheHandler
from spotipy.oauth2 import SpotifyClientCredentials

import config
from models import *

if config.sentryDSN:
    client = sentry_sdk.init(dsn=config.sentryDSN)


class RedisCacheHandler(CacheHandler):
    """
    based on https://github.com/plamere/spotipy/pull/747
    """

    def __init__(self, redis):
        self.redis = redis

    def get_cached_token(self):
        token_info = self.redis.get('token_info')
        if token_info:
            return json.loads(token_info)

    def save_token_to_cache(self, token_info):
        self.redis.set('token_info', json.dumps(token_info))


r = Redis(db=config.redisDB)
crm = SpotifyClientCredentials(**config.spotify, cache_handler=RedisCacheHandler(r))
sp = spotipy.Spotify(client_credentials_manager=crm, requests_session=False)

if len(sys.argv) > 1:
    limit = int(sys.argv[1])
else:
    limit = 50

query = Song.select().where((Song.show == 0))
if not len(sys.argv) > 3 or sys.argv[2] != "force":
    query = query.where(Song.spotify_data.is_null())
else:
    starting = int(sys.argv[3])
    print("fetching empty starting from {id}".format(id=starting))
    query = query.where((Song.spotify_data == 0) & (Song.id >= starting))
for song in query.limit(limit):
    song.title = song.title.replace("+", " ")
    print(song.title)
    if song.artist.isupper():
        song.artist = song.artist.title()
    if song.title.isupper():
        song.title = song.title.title()
    print(song.id)
    sleep(0.1)
    searchtitle = re.sub("[\(\[].*?[\)\]]", "", song.title)
    searchartist = song.artist.replace("&", "").replace("Feat.", "")
    results = sp.search(q=searchtitle + ' ' + searchartist, type='track', limit=1)
    if len(results["tracks"]["items"]) == 0:
        song.spotify_data = False
        print("not found")
    else:
        print("found")
        track = results["tracks"]["items"][0]
        song.spotify_url = track["external_urls"]["spotify"]
        song.preview_url = track["preview_url"]
        images = track["album"]["images"]
        if len(images):
            song.image_large = images[0]["url"]
            song.image_small = images[-1]["url"]
        song.spotify_data = True

        # print(song.title)
        # print(track["name"])
        # print(song.artist)
        # print(", ".join([a["name"] for a in track["artists"]]))

    song.save()
