from flask import jsonify
from playhouse.shortcuts import model_to_dict

from app import app
from models import *


def query_to_response(query, limit=5, **kwargs):
    """

    :param limit: int|boolean
    :param **kwargs
    :type query: peewee.ModelSelect
    """
    if limit:
        query = query.limit(limit)
    print(query.sql())
    data = []
    for i in query:
        data.append(model_to_dict(i, **kwargs))
    return jsonify(data)


@app.route('/')
def index():
    return query_to_response(Channel.select(), limit=False)


@app.route('/<channel>')
def popular(channel):
    # range = request.args.get('')
    get = Play.select(Play.song, fn.Count(SQL('*')).alias("magnitude")) \
        .join(Channel).switch(Play).join(Song) \
        .where((Song.show == 0) & (Channel.shortname == channel)) \
        .group_by(Play.song).order_by(SQL('magnitude').desc())
    return query_to_response(get, extra_attrs=["magnitude"])


if __name__ == '__main__':
    app.run()
