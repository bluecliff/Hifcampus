#!/bin/bash 
killall -s HUP uwsgi
uwsgi -s 127.0.0.1:9001 -w manage:app -d ./uwsgi.log
