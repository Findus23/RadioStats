from bs4 import BeautifulSoup

from utils import *


def get(channel):
    url = "http://www.energy.at/extern/tifo/?station=vie&hour={hour}&min={min}&date={date}&submit=1"
    now = datetime.now() - timedelta(minutes=30)
    url = url.format(hour=now.hour, min=now.minute, date=now.strftime("%d.%m.%Y"))
    soup = BeautifulSoup(fetch(url, False), 'html.parser')
    print(url)
    for item in soup.findAll("div", "item"):
        artist = item.find("p", "interpret").get_text()
        title = item.find("p", "title").get_text()
        timestring = item.find("span", "time").get_text()
        datestring = item.find("span", "date").get_text()
        time = local_to_utc(datetime.strptime(datestring + " " + timestring, '%d.%m.%Y %H:%M'))
        yield time, artist, title
    exit()
