'''
Created on 22 oct. 2012

@author: herve
'''

from peewee import *

db = SqliteDatabase(':memory:', autocommit=False)


class User(Model):
    username = CharField()

    class Meta:
        database = db


class Tweet(Model):
    user = ForeignKeyField(User, related_name='tweets')
    message = TextField()

    class Meta:
        database = db

db.connect()
User.create_table()
Tweet.create_table()
