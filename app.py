# Blog configuration values.

import logging

from flask import Flask
from playhouse.flask_utils import FlaskDB
from playhouse.pool import PooledMySQLDatabase
from raven.contrib.flask import Sentry

import config

DATABASE = PooledMySQLDatabase("radio", **config.db)

# Create a Flask WSGI app and configure it using values from the module.
app = Flask(__name__)
app.config.from_object(__name__)

if config.sentryDSN:
    sentry = Sentry(app, dsn=config.sentryDSN, logging=True, level=logging.WARNING)

flask_db = FlaskDB(app)

db = flask_db.database
