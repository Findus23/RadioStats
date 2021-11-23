import json

from websocket import create_connection, WebSocket

from parser import BaseFetcher
from utils import *

URL = "wss://www.arabella.at/api/_socket/"


class ArabellaFetcher(BaseFetcher):
    def get(self, channel):
        ws: WebSocket = create_connection(URL, suppress_origin=True)
        init = ws.recv()

        ws.send(json.dumps({"type": "select_channels", "channelIds": [1]}))

        result = ws.recv()
        ws.close()
        data = json.loads(result)
        tracks = [data["currentTrack"]]
        tracks.extend(data["previousTracks"])
        tracks.extend(data["futureTracks"])
        for track in tracks:
            artist = track["artist"]
            title = track["title"]
            time = time_to_date(string_to_time(track["time"], seconds=False))
            yield time, artist, title
