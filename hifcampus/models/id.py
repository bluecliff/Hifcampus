#!/usr/bin/env python
# encoding: utf-8

from hifcampus import db
from hifcampus import config
class Id(db.Document):
    uid = db.IntField(default=config.DEFAULT_ID)
    newsid = db.IntField(default=config.DEFAULT_ID)
    newscateid = db.IntField(default=config.DEFAULT_ID)
    activityid = db.IntField(default=config.DEFAULT_ID)
    jobid=db.IntField(default=config.DEFAULT_ID)
    commentid = db.IntField(default=config.DEFAULT_ID)
    personid = db.IntField(default=config.DEFAULT_ID)
    imageid = db.IntField(default=config.DEFAULT_ID)
    lectureid = db.IntField(default=config.DEFAULT_ID)
    @classmethod
    def get_next_id(self,which):
        if len(Id.objects) > 0:
            i = Id.objects.first()
            i._data[which]=i._data[which]+1
            i._changed_fields.append(which)
        else:
            i = Id()
        i.save()
        return i._data[which]
