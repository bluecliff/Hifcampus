#!/usr/bin/env python
# encoding: utf-8

from hifcampus import db
from flask.ext.login import UserMixin
import datetime
class Hifuser(db.Document,UserMixin):
    """User model"""
    id = db.IntField(primary_key=True,verbose_name=u"ID")
    nickname = db.StringField(unique=True,default="",required=True,verbose_name=u"昵称")
    password = db.StringField(required=True,default="",verbose_name=u"密码")
    thumbnail = db.IntField(default=0,verbose_name=u"是否有头像")
    email = db.EmailField(required=True,default="",verbose_name=u"邮箱")
    create_time = db.DateTimeField(default=datetime.datetime.utcnow(),verbose_name=u"创建时间")
    last_login = db.DateTimeField(default=datetime.datetime.utcnow(),verbose_name=u"上次登录")
    permission = db.StringField(default="user",verbose_name=u"权限")
    def get_id(self):
        return str(self.id)+":"+self.password
    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def __repr__(self):
        return self.nickname
    def __unicode__(self):
        return self.nickname
    meta = {
        'ordering': ['-id']
    }
