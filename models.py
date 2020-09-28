from peewee import CharField, BooleanField, DateTimeField, ForeignKeyField

from basemodel import BaseModel


class Channel(BaseModel):
    shortname = CharField(unique=True, max_length=5)
    stationname = CharField()
    has_data = BooleanField()
    primary_color = CharField(max_length=7)
    secondary_color = CharField(max_length=7)


class Song(BaseModel):
    artist = CharField(max_length=150)
    title = CharField(max_length=150)
    show = BooleanField()
    spotify_data = BooleanField(null=True)
    preview_url = CharField(null=True)
    spotify_url = CharField(null=True)
    image_small = CharField(null=True)
    image_large = CharField(null=True)
    background_color = CharField(null=True, max_length=6)
    alternative_color = CharField(null=True, max_length=6)
    text_color = CharField(null=True, max_length=6)

    class Meta:
        indexes = ((("artist", "title"), True),)


class Play(BaseModel):
    song = ForeignKeyField(Song)
    channel = ForeignKeyField(Channel)
    time = DateTimeField()

    class Meta:
        indexes = ((("time", "channel"), True),)
