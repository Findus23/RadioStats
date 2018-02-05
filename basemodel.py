from peewee import Model, MySQLDatabase

import config

db = MySQLDatabase("radio", **config.db)

db.connect()


class BaseModel(Model):
    class Meta:
        database = db
