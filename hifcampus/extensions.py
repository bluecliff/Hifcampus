#!/usr/bin/env python
# encoding: utf-8

from flask.ext.mongoengine import MongoEngine
db = MongoEngine()

from flask.ext.login import LoginManager,current_user
login_manager = LoginManager()

from flask.ext.principal import Principal,identity_loaded,RoleNeed,UserNeed,Permission
def init_principal(app):
    principal=Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender,identity):
        identity.user=current_user
        if hasattr(current_user,'id'):
            identity.provides.add(UserNeed(current_user.id))
        if hasattr(current_user,'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(ROLE[role]))


permissions = {
    'user': Permission(RoleNeed('admin'),RoleNeed('user')),
    'news': Permission(RoleNeed('admin'),RoleNeed('news_admin')),
    'activity': Permission(RoleNeed('admin'),RoleNeed('activity_admin')),
    'lecture': Permission(RoleNeed('admin'),RoleNeed('lecture_admin')),
    'job': Permission(RoleNeed('admin'),RoleNeed('job_admin')),
    'grapevine': Permission(RoleNeed('admin'),RoleNeed('grapevine_admin')),
    'express': Permission(RoleNeed('admin'),RoleNeed('express_admin')),
    'weekperson': Permission(RoleNeed('admin'),RoleNeed('person_admin')),
    'admin':Permission(RoleNeed('admin')),
}

#user role
ADMIN = 0
USER=1
NEWS_ADMIN=2
LECTURE_ADMIN=3
JOB_ADMIN=4
WEEKPERSON_ADMIN=5
ACTIVITY_ADMIN=6

ROLE={
    ADMIN:'admin',
    USER:'user',
    NEWS_ADMIN:'news_admin',
    LECTURE_ADMIN:'lecture_admin',
    JOB_ADMIN:'job_admin',
    WEEKPERSON_ADMIN:'weekperson_admin',
    ACTIVITY_ADMIN:'activity_admin',
}
