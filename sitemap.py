from peewee import SQL, fn

xml = """
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

from models import Channel, Play, Song

for channel in Channel.select().where(Channel.has_data == 1):
    xml += """
<url>
    <loc>https://radiostats.lw1.at/{channel}</loc>
</url>
""".format(channel=channel.shortname)
    get = Play.select(Play.song, Song.id, fn.Count(SQL('*')).alias("count")) \
        .join(Channel).switch(Play).join(Song) \
        .where((Song.show == 0) & (Channel.shortname == channel.shortname)) \
        .group_by(Play.song).order_by(SQL('count').desc()).limit(500)
    for i in get:
        song = i.song.id
        xml += """
<url>
    <loc>https://radiostats.lw1.at/{channel}/song/{songid}</loc>
</url>
""".format(channel=channel.shortname, songid=song)

xml += "</urlset>"

with open('sitemap.xml', 'w') as file:
    file.write(xml)
