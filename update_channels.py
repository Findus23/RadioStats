import channelInfo
from models import Channel

for id, channel in channelInfo.channels.items():
    print("update", channel.stationname)

    db_chan = Channel.get(shortname=channel.shortname)
    db_chan.stationname = channel.stationname
    db_chan.has_data = channel.has_data
    db_chan.primary_color = channel.primary_color
    db_chan.secondary_color = channel.secondary_color
    db_chan.save()
