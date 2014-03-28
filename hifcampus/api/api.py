#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint,abort,current_app as app,send_from_directory,request,jsonify
from hifcampus.models import Hiflecture,Hifnews,Model,add_comment,get_detail


bp_api = Blueprint('bp_api',__name__,url_prefix='/api')


ERROR_MESSAGE={
        'ERROR_REQUEST':{'msg':3000,'detail':'invalid request'},
        'ERROR_NOMORE':{'msg':3001,'detail':'no more items'},
        'ERROR_NOITEM':{'msg':3002,'detail':'no this item'},
        'ERROR_INSERT':{'msg':3003,'detaic':'failed to add item'},
        }
SUCCCESS_MESSAGE={
        'INSERT_SUCCESS':{'msg':1,'detail':'add item successfully'},
        }
@bp_api.route("/list/<model>/",defaults={'perpage':10,'id':0},methods=["GET",])
@bp_api.route("/list/<model>/<int:id>/",defaults={'perpage':10},methods=["GET",])
@bp_api.route("/list/<model>/<int:perpage>/<int:id>/",methods=["GET",])
def list(model,perpage,id):
    res = {}
    res['msg']=0
    if not Model.has_key(model):
        return jsonify(ERROR_MESSAGE['ERROR_REQUEST'])
    reslist = Model[model].getlist(id,perpage)
    if len(reslist) == 0:
        return jsonify(ERROR_MESSAGE['ERROR_NOMORE'])
    else:
        res['data'] = reslist
        return jsonify(res)

@bp_api.route("/detail/<model>/<int:id>/",methods=["GET",])
def detail(model,id):
    res = get_detail(model,id)
    if res is None:
        return jsonify(ERROR_MESSAGE['ERROR_REQUEST'])
    else:
        return jsonify(get_detail(model,id))

@bp_api.route("/thumbnail/<size>/<int:id>/",methods=["GET",])
def thumbnail(size,id):
    file_name=str(id)+'_'+str(size)+'.png'
    return send_from_directory(app.config['THUMBNAIL_PATH'],file_name)

@bp_api.route("/comment/<model>/<int:id>/",methods=["POST",])
def post_comment(model,id):
    print '11'
    if not request.json:
        return jsonify(ERROR_MESSAGE['ERROR_POST'])
    if add_comment(model,id,request.json):
        return jsonify(SUCCCESS_MESSAGE['INSERT_SUCCESS'])
    else:
        return jsonify(ERROR_MESSAGE['INSERT_FAIL'])
