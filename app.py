# Blog configuration values.

import sentry_sdk
from flask import Flask
from flask_caching import Cache
from playhouse.flask_utils import FlaskDB
from playhouse.pool import PooledMySQLDatabase
from sentry_sdk.integrations.flask import FlaskIntegration

import config

DATABASE = PooledMySQLDatabase("radio", **config.db)
if config.cache:
    CACHE_TYPE = "redis"
else:
    CACHE_TYPE = "null"
CACHE_REDIS_DB = config.redisDB

if config.sentryDSN:
    sentry_sdk.init(
        dsn=config.sentryDSN,
        integrations=[FlaskIntegration()]
    )

# Create a Flask WSGI app and configure it using values from the module.
app = Flask(__name__)
app.config.from_object(__name__)
cache = Cache(app)

flask_db = FlaskDB(app)

db = flask_db.database
