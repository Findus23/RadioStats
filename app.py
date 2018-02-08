# Blog configuration values.

from flask import Flask
from peewee import MySQLDatabase
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list

import config

DATABASE = MySQLDatabase("radio", **config.db)


# Create a Flask WSGI app and configure it using values from the module.
app = Flask(__name__)
app.config.from_object(__name__)

flask_db = FlaskDB(app)

db = flask_db.database

