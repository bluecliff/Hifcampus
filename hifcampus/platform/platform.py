#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint,render_template,request,redirect,url_for,current_app as app,g,abort,session,send_from_directory
import json,traceback
from hifcampus import config,utils
from hifcampus.models import Hifuser,Hifnews,Hifactivity,Hifweekperson,Hiflecture,Hifjob,Hifgrapevine
from flask.ext.principal import IdentityContext,identity_changed,Identity,AnonymousIdentity,Permission,RoleNeed
from flask.ext.login import current_user,login_required,logout_user,login_user
from werkzeug import check_password_hash,generate_password_hash


bp_platform = Blueprint(
    "bp_platform",
    __name__,
    url_prefix='/platform')

@bp_platform.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("platform/index.html")

@bp_platform.route("/thumbnail/<id>/<type>",methods=["GET"])
def get_thumbnail(id,type):
    file_name=str(id)+'_'+str(type)+'.png'
    return send_from_directory(app.config['THUMBNAIL_PATH'],file_name)

Model={
        'news':Hifnews,
        'activity':Hifactivity,
        'job':Hifjob,
        'lecture':Hiflecture,
        'user':Hifuser,
        'grapevane':Hifgrapevine,
        'person':Hifweekperson,
    }
@bp_platform.route("/changestatus/<model>/<postid>",methods=["GET","POST"])
@login_required
def changestatus(model,postid):
    res={}
    res['msg']=0
    try:
        item = Model[model].objects.get(id=postid)
        if item.status==0:
            item.status=1
        else:
            item.status=0
        item.save()
        return json.dumps(res)
    except:
        traceback.print_exc()
        res['msg']=2001
        res['msgdetail']=u"更新失败"
        return json.dumps(res)
@bp_platform.route("/delete/<model>/<postid>",methods=["GET","POST"])
@login_required
def item_del(model,postid):
    res={}
    res['msg']=0
    try:
        Model[model].objects(id=postid).delete()
    except:
        traceback.print_exc()
        res['msg'] = 2000
        res['msg_detail']=u"删除失败"
    return json.dumps(res)

from flask.views import MethodView

def check_permission(permission_item):
    try:
        if not g.identity.can(permission_item):
            abort(401)
    except:
        abort(401)

class PlatformView(MethodView):
    '''Pluggable List View with pagination
    '''
    def __init__(self):
        self.permission  = None

    def get_template_name(self):
        raise NotImplementedError()

    def get_model(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def get(self, *args, **kwargs):
        if not current_user or not current_user.is_authenticated():
            return redirect(url_for(".login"))
        if 'permission' in kwargs['args']:
            check_permission(kwargs['args']['permission'])
        if 'model' in kwargs['args']:
            self.model = kwargs['args']['model']
        context = {'objects': self.get_objects(*args, **kwargs)}
        if not 'fields' in kwargs['args']:
            kwargs['args']['fields'] = self.get_model()._fields.keys()
        context.update(kwargs)
        return self.render_template(context)

    def post(self, *args, **kwargs):
        abort(401)

    def get_objects(self, *args, **kwargs):
        raise NotImplementedError()

from list import add_list_views,LIST
from .edit import add_edit_views,EDIT
add_list_views(LIST)
add_edit_views(EDIT)
