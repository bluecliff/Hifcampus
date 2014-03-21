#!/usr/bin/env python
# encoding: utf-8

import string
import os

INSTANCE_FOLDER_PATH=os.path.join('/tmp','instance')

def makedir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception,e:
        raise e
PASSWORD_LEN_MAX=20
PASSWORD_LEN_MIN=6
USERNAME_LEN_MAX=20
USERNAME_LEN_MIN=5

