import __main__
from peewee import Model, MySQLDatabase

import config

if __main__.__file__ != "server.py":
    db = MySQLDatabase("radio", **config.db)
    db.connect()
else:
    from app import db


class BaseModel(Model):
    class Meta:
        database = db
