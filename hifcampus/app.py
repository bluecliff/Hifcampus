#!/usr/bin/env python
# encoding: utf-8

import os
from flask import Flask
from .config import DefaultConfig
from models import Hifuser
from .extensions import db,login_manager,init_principal,permissions
from .utils import INSTANCE_FOLDER_PATH
from .extensions import ROLE
from platform import bp_platform
from user import bp_user

__all__= ['create_app']

DEFAULT_BLUEPRINTS=(
        bp_platform,
        bp_user,
        )

def create_app(config=None,app_name=None,blueprints=None):
    """create an app"""
    if app_name is None:
        app_name=DefaultConfig.PROJECT
    if blueprints is None:
        blueprints=DEFAULT_BLUEPRINTS

    app = Flask(app_name,instance_path=INSTANCE_FOLDER_PATH,instance_relative_config=True)
    configuer_app(app,config)
    configuer_hook(app)
    configure_blueprints(app,blueprints)
    configure_extensions(app)
    configuer_template(app)
    configuer_context_processor(app)
    return app

def configuer_app(app,config=None):
    app.config.from_object(DefaultConfig)
    app.config.from_pyfile('production.cfg',silent=True)

    if config:
        app.config.from_object(config)

def configuer_hook(app):
    @app.before_request
    def before_request():
        pass
def configure_blueprints(app,blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
def configure_extensions(app):
    db.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Hifuser.objects(id=id).first()
    login_manager.init_app(app)

    init_principal(app)
#    principal.init_app(app)

def configuer_template(app):
    @app.template_filter()
    def format_date(value,format='%Y-%m-%d'):
        return value.strftime(format)
    @app.template_filter()
    def format_role(value):
        role=[]
        for role_id in value:
            role.append(ROLE[role_id])
        return role

def configuer_context_processor(app):
    @app.context_processor
    def permission_check():
        def allow(permission):
            return permissions[permission].can()
        return dict(allow=allow)
