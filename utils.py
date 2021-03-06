import sys
from datetime import datetime, timedelta, time
from time import sleep

import pytz
import requests
from requests import Response

s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (compatible; RadioStats/1.0;)',
})


def careful_fetch(url) -> Response:
    """
    :rtype: requests.models.Response
    """
    print(url)
    result = None
    tries = 0
    while result is None:
        try:
            req = s.get(url)
            if "Invalid resource" in req.text:
                raise requests.exceptions.ConnectionError
            return req

        except requests.exceptions.ConnectionError:
            print("404")
            tries += 1
            if tries >= 3:
                raise Exception("too many retries")
            sleep(1)
            pass


def string_to_time(timestring, seconds=True) -> time:
    if seconds:
        format = "%H:%M:%S"
    else:
        format = "%H:%M"
    return datetime.strptime(timestring, format).time()


def time_to_date(time: time) -> datetime:
    time_hour = time.hour
    day = datetime.now()
    current_hour = day.hour

    if 0 <= current_hour <= 3 and 22 <= time_hour <= 24:
        day = datetime.today() - timedelta(days=1)

    local = datetime.combine(day.date(), time)
    return local_to_utc(local)


def local_to_utc(date):
    tz = pytz.timezone("Europe/Vienna")
    local_dt = tz.localize(date)
    return local_dt.astimezone(pytz.utc)


def fetch(url, json=False):
    req = s.get(url)
    if req.status_code != 200:
        print("URL failed to fetch: {status} {url}".format(status=req.status_code, url=url), file=sys.stderr)
        return False
    if json:
        return req.json()
    return req.text
