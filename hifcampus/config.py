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
    makedir(UPLOAD_FOLDER)

class DefaultConfig(BaseConfig):
    DEBUG=True
    MONGODB_SETTINGS ={
        "DB":"HifTest",
        "host":"localhost",
        "port":10001,
        }



