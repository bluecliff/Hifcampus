#!/usr/bin/env python
# encoding: utf-8

from hifcampus.extensions import db
from user import Hifuser
import datetime

class Hifcomment(db.Document):
    """Comment model"""
    id = db.IntField(primary_key=True)
    author = db.ReferenceField(Hifuser)
    content = db.StringField()
    create_time = db.DateTimeField(default=datetime.datetime.utcnow())
    meta = {
        'ordering': ['+create_time']
    }
