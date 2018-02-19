import calendar
from datetime import datetime, timedelta

from flask import jsonify, request
from playhouse.shortcuts import model_to_dict

from app import app
from models import *


def query_to_response(query, limit=10, key=False, sort=False, offset=None, list=None, **kwargs):
    """

    :param sort: boolean
    :param offset: int
    :type key: str
    :type limit: int|boolean
    :param **kwargs
    :type query: peewee.ModelSelect
    """
    if limit:
        query = query.limit(limit)
    print(query.sql())
    data = {} if key is not False else []
    order = int(offset) if offset else 0
    for i in query:
        element = model_to_dict(i, **kwargs)
        if list:
            element = element[list]
        if sort:
            element["order"] = order
            order += 1
        if key is not False:
            if "." in key:
                key1, key2 = key.split(".")
                data[getattr(getattr(i, key1), key2)] = element
            else:
                data[getattr(i, key)] = element
        else:
            data.append(element)
    response = jsonify(data)
    if __name__ == '__main__':
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/')
def index():
    return query_to_response(Channel.select(), limit=False, key="shortname")


def get_range(date, date_type):
    if date_type == "day":
        start = date
        end = date
    elif date_type == "week":
        start = date - timedelta(days=date.weekday())
        end = start + timedelta(days=6)
    elif date_type == "month":
        start = date.replace(day=1)
        end = date.replace(day=calendar.monthrange(date.year, date.month)[1])
    else:
        start = datetime.strptime("2000-01-01", '%Y-%m-%d')
        end = datetime.strptime("2050-01-01", '%Y-%m-%d')
    end = end + timedelta(days=1)
    return start, end


def get_dates_from_request():
    try:
        date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')
        date_type = request.args.get('dateType')
        if date_type not in ["day", "week", "month", "alltime"]:
            raise ValueError
    except (TypeError, ValueError):
        date = datetime.today()
        date_type = "month"
    return date, date_type


@app.route('/api/<channel>')
def popular(channel):
    date, date_type = get_dates_from_request()
    start, end = get_range(date, date_type)
    get = Play.select(Play.song, fn.Count(SQL('*')).alias("count")) \
        .join(Channel).switch(Play).join(Song) \
        .where((Song.show == 0) & (Channel.shortname == channel) & (
        Play.time.between(start, end))) \
        .group_by(Play.song).order_by(SQL('count').desc())
    if request.args.get('offset'):
        get = get.offset(int(request.args.get('offset')))
    return query_to_response(get, extra_attrs=["count"], exclude=[Play.channel, Play.time, Play.id], key="song.id",
                             sort=True, offset=request.args.get('offset'))


@app.route('/api/<channel>/plays/<song_id>')
def plays(channel, song_id):
    date, date_type = get_dates_from_request()
    start, end = get_range(date, date_type)
    get = Play.select(Play.time) \
        .join(Channel) \
        .where((Play.song == song_id) & (Channel.shortname == channel) & (Play.time.between(start, end)))\
        .order_by(Play.time.desc())
    return query_to_response(get, exclude=[Play.channel, Play.song, Play.id], list="time", limit=False)


if __name__ == '__main__':
    app.debug = True
    app.run()
