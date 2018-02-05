from peewee import *

from basemodel import BaseModel


class Channel(BaseModel):
    shortname = CharField(unique=True, max_length=5)
    streamurl = CharField()
    stationname = CharField()
    supports_json = BooleanField()


class Song(BaseModel):
    artist = CharField(max_length=150)
    title = CharField(max_length=150)
    show = BooleanField()

    class Meta:
        indexes = ((("artist", "title"), True),)


class Play(BaseModel):
    song = ForeignKeyField(Song)
    channel = ForeignKeyField(Channel)
    time = DateTimeField()

    class Meta:
        indexes = ((("time", "channel"), True),)
