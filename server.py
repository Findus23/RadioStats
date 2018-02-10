import calendar
from datetime import datetime, timedelta

from flask import jsonify, request
from playhouse.shortcuts import model_to_dict

from app import app
from models import *


def query_to_response(query, limit=10, key=False, **kwargs):
    """

    :type key: str
    :type limit: int|boolean
    :param **kwargs
    :type query: peewee.ModelSelect
    """
    if limit:
        query = query.limit(limit)
    print(query.sql())
    data = {} if key is not False else []
    for i in query:
        element = model_to_dict(i, **kwargs)
        if key is not False:
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


def getRange(date, date_type):
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


@app.route('/api/<channel>')
def popular(channel):
    try:
        date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')
        date_type = request.args.get('dateType')
        if date_type not in ["day", "week", "month", "alltime"]:
            raise ValueError
    except (TypeError, ValueError):
        date = datetime.today()
        date_type = "month"
    start, end = getRange(date, date_type)
    get = Play.select(Play.song, fn.Count(SQL('*')).alias("count")) \
        .join(Channel).switch(Play).join(Song) \
        .where((Song.show == 0) & (Channel.shortname == channel) & (
        Play.time.between(start, end))) \
        .group_by(Play.song).order_by(SQL('count').desc())
    if request.args.get('offset'):
        get = get.offset(int(request.args.get('offset')))
    return query_to_response(get, extra_attrs=["count"], exclude=[Play.channel, Play.time, Play.id])


if __name__ == '__main__':
    app.debug = True
    app.run()
