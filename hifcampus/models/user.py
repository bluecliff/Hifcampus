#!/usr/bin/env python
# encoding: utf-8

from hifcampus.extensions import db
from flask.ext.login import UserMixin
import datetime
from werkzeug import check_password_hash,generate_password_hash
from hifcampus import constants as USER
class Hifuser(db.Document,UserMixin):
    """User model"""
    id = db.IntField(primary_key=True,verbose_name=u"ID")
    nickname = db.StringField(unique=True,default="",verbose_name=u"昵称")
    password = db.StringField(default="",verbose_name=u"密码")
    avatar = db.IntField(default=0,verbose_name=u"是否有头像")
    email = db.EmailField(unique=True,default="",verbose_name=u"邮箱")
    create_time = db.DateTimeField(default=datetime.datetime.utcnow(),verbose_name=u"创建时间")
    last_login = db.DateTimeField(default=datetime.datetime.utcnow(),verbose_name=u"上次登录")
    #permission = db.StringField(default="user",verbose_name=u"权限")
    role = db.IntField(default=USER.USER,verbose_name=u"ROLE")

    @classmethod
    def authenticate(cls,username,password):
        user = cls.objects(nickname=username).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated=False
        return user,authenticated
    def get_id(self):
        return unicode(self.id)
    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def check_password(self,password):
        if self.password is None:
            return False
        else:
            return check_password_hash(self.password,password)
    def get_role(self):
        return USER.ROLE[self.role]
    def __repr__(self):
        return self.nickname
    def __unicode__(self):
        return self.nickname
    meta = {
        'ordering': ['-id']
    }
