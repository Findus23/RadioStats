from datetime import datetime, timedelta
from time import sleep

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; RadioStats/1.0;)',
}


def careful_fetch(url):
    """
    :rtype: requests.models.Response
    """
    print(url)
    result = None
    tries = 0
    while result is None:
        try:
            req = requests.get(url, headers=headers)
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


def string_to_time(timestring):
    """

    :rtype: datetime.time
    """
    return datetime.strptime(timestring, "%H:%M:%S").utcnow().time()


def time_to_date(time):
    """

    :rtype: datetime.datetime
    :type time: datetime.time
    """
    time_hour = time.hour
    day = datetime.now()
    current_hour = day.hour

    if 0 <= current_hour <= 3 and 22 <= time_hour <= 24:
        day = datetime.today() - timedelta(days=1)

    return datetime.combine(day.date(), time)


def fetch(url, json=False):
    req = requests.get(url, headers=headers)
    if json:
        return req.json()
    return req.text
