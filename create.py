import json

import requests

from models import *

for i in [Play, Channel, Song]:
    i.drop_table()
for i in [Channel, Song, Play]:
    i.create_table()

r = requests.get('http://radio.orf.at/player/js/config.js')
config_js = r.text
pseudo_json = config_js \
    .replace("// here be the settings for all radio programs", "") \
    .replace("var stations = ", "") \
    .replace("};", "}") \
    .replace("Burgenland\",", "Burgenland\"")

config = json.loads(pseudo_json)

for id, channel in config.items():
    if id != "validStationList" and "apasf.sf.apa.at" in channel["streamurl"] and id != "oe1":
        streamurl = channel["streamurl"].replace(";", "")
        try:
            r = requests.get(streamurl + "played.html?type=json")
            supports_json = r.status_code == 200
        except requests.exceptions.ConnectionError:
            supports_json = False
        Channel.get_or_create(shortname=channel["shortname"], streamurl=streamurl,
                              stationname=channel["stationname"], supports_json=supports_json)
