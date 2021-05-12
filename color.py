import json
import sys
import tempfile
from pathlib import Path
from subprocess import run
from time import sleep

import requests
import sentry_sdk
from peewee import fn

import config
from models import *


def to_rgb_string(r: float, g: float, b: float) -> str:
    r, g, b = map(int, [r, g, b])
    return "{0:02x}{1:02x}{2:02x}".format(r, g, b)


cwd = Path(__file__).resolve().parent
colorjs = cwd / Path("./web/color.js")

if config.sentryDSN:
    client = sentry_sdk.init(dsn=config.sentryDSN)

if len(sys.argv) > 1:
    limit = int(sys.argv[1])
else:
    limit = 50

query = Song.select().where(
    (Song.show == 0) & (Song.spotify_data == 1) & (Song.image_large.is_null(False)) & (Song.background_color.is_null()))
for song in query.order_by(fn.Rand()).limit(limit):
    print(song.title)
    url = song.image_large
    print(url)
    if not url:
        continue

    r = requests.get(url)
    if r.status_code == 404:
        song.spotify_data = None
        song.save()
        continue
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)
        image = tmpdir / "image.jpg"
        with open(image, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        output = run(["node", colorjs, image], capture_output=True)
        data = json.loads(output.stdout)
    song.background_color = to_rgb_string(*data["LightVibrant"]["rgb"]) if "LightVibrant" in data else None
    song.alternative_color = to_rgb_string(*data["DarkVibrant"]["rgb"]) if "DarkVibrant" in data else None
    song.text_color = to_rgb_string(*data["DarkMuted"]["rgb"]) if "DarkMuted" in data else None
    song.save()
    print(song.background_color)
    print(song.alternative_color)
    print(song.text_color)
    sleep(5)
