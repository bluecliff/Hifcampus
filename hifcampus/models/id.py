#!/usr/bin/env python
# encoding: utf-8

from ..extensions import db
from hifcampus.constants import DEFAULT_ID
class Id(db.Document):
    uid = db.IntField(default=DEFAULT_ID)
    newsid = db.IntField(default=DEFAULT_ID)
    newscateid = db.IntField(default=DEFAULT_ID)
    activityid = db.IntField(default=DEFAULT_ID)
    jobid=db.IntField(default=DEFAULT_ID)
    commentid = db.IntField(default=DEFAULT_ID)
    personid = db.IntField(default=DEFAULT_ID)
    imageid = db.IntField(default=DEFAULT_ID)
    lectureid = db.IntField(default=DEFAULT_ID)
    grapevineid=db.IntField(default=DEFAULT_ID)
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
