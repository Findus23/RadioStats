import channelInfo
from models import *

for i in [Play, Channel, Song]:
    i.drop_table()
for i in [Channel, Song, Play]:
    i.create_table()

for id, channel in channelInfo.channels.items():
    if "streamurlShoutcast2" in channel:
        streamurl = channel["streamurlShoutcast2"].replace(";", "")
    else:
        streamurl = None
    if "cStationName" in channel:
        channel["stationname"] = channel["cStationName"]
    Channel.create(shortname=channel["shortname"], streamurl=streamurl,
                   stationname=channel["stationname"], has_data=channel["cHasData"],
                   primary_color=channel["cPrimaryColor"], secondary_color=channel["cSecondaryColor"])
