import channelInfo
from models import *

for i in [Play, Channel, Song]:
    i.drop_table()
for i in [Channel, Song, Play]:
    i.create_table()

for id, channel in channelInfo.channels.items():
    print("create", channel.stationname)
    Channel.create(shortname=channel.shortname, stationname=channel.stationname, has_data=channel.has_data,
                   primary_color=channel.primary_color, secondary_color=channel.secondary_color)
