from flask import jsonify, request
from playhouse.shortcuts import model_to_dict

from app import app
from models import *


def query_to_response(query, limit=5, key=False, **kwargs):
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


@app.route('/api/<channel>')
def popular(channel):
    # range = request.args.get('')
    get = Play.select(Play.song, fn.Count(SQL('*')).alias("count")) \
        .join(Channel).switch(Play).join(Song) \
        .where((Song.show == 0) & (Channel.shortname == channel)) \
        .group_by(Play.song).order_by(SQL('count').desc())
    if request.args.get('offset'):
        print(request.args.get('offset'))
        get = get.offset(int(request.args.get('offset')))
    return query_to_response(get, extra_attrs=["count"], exclude=[Play.channel, Play.time, Play.id])


if __name__ == '__main__':
    app.debug = True
    app.run()
