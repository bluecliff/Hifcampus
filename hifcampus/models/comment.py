#!/usr/bin/env python
# encoding: utf-8

from hifcampus import db
from hifcampus.models import Hifuser
import datetime

class Hifcomments(db.Document):
    """Comment model"""
    id = db.IntField(primary_key=True)
    author = db.ReferenceField(Hifuser)
    content = db.StringField()
    create_time = db.DateTimeField(default=datetime.datetime.utcnow())
    meta = {
        'ordering': ['+create_time']
    }
