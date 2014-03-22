#!/usr/bin/env python
# encoding: utf-8

import os
from flask import request,Flask,render_template
from .config import DefaultConfig
from models import Hifuser
from user import user
#from .settings import settings
from .extensions import db,login_manager,init_principal
from .utils import INSTANCE_FOLDER_PATH

__all__= ['create_app']

DEFAULT_BLUEPRINTS=(
        user,
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

