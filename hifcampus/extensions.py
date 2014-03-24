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

from constants import ROLE
permissions={}
for (key,value) in ROLE.iteritems():
    permissions[key]=Permission(RoleNeed(value))
