# Blog configuration values.

import logging

from flask import Flask
from flask_caching import Cache
from playhouse.flask_utils import FlaskDB
from playhouse.pool import PooledMySQLDatabase
from raven.contrib.flask import Sentry

import config

DATABASE = PooledMySQLDatabase("radio", **config.db)
if config.cache:
    CACHE_TYPE = "redis"
else:
    CACHE_TYPE = "null"
CACHE_REDIS_DB = config.redisDB

# Create a Flask WSGI app and configure it using values from the module.
app = Flask(__name__)
app.config.from_object(__name__)
cache = Cache(app)

if config.sentryDSN:
    sentry = Sentry(app, dsn=config.sentryDSN, logging=True, level=logging.WARNING)

flask_db = FlaskDB(app)

db = flask_db.database
