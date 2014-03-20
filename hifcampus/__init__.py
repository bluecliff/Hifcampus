#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    return app
