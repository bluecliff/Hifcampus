#!/usr/bin/env python
# encoding: utf-8

import os
from utils import makedir,INSTANCE_FOLDER_PATH

class BaseConfig(object):
    PROJECT='hifcampus'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DEBUG=False

    DEFAULT_ID=1000
    JSONIFY_PRETTYPRINT_REGULAR=True
    SECRET_KEY="lijsf"

    UPLOAD_FOLDER=os.path.join(PROJECT_ROOT,'uploads')
    THUMBNAIL_PATH=os.path.join(UPLOAD_FOLDER,'thumbnail')
    makedir(UPLOAD_FOLDER)
    makedir(THUMBNAIL_PATH)

class DefaultConfig(BaseConfig):
    DEBUG=True
    MONGODB_SETTINGS ={
        "DB":"hifcampus_new",
       # "host":"localhost",
       # "port":10001,
        }



