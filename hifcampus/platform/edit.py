#!/usr/bin/env python
# encoding: utf-8

from .platform import PlatformView
from hifcampus.extensions import permissions
from hifcampus.models import Hifuser,Hifactivity,Hifnews,Hiflecture,Hifjob,Hifweekperson,Id,Hifgrapevine
from wtforms import widgets
from flask import abort,request,url_for,redirect,current_app as app
from .platform import bp_platform,check_permission
from flask.ext.mongoengine.wtf import model_form
from flask.ext.login import current_user
from hifcampus import utils
from hifcampus.extensions import ROLE
import traceback
import datetime

EDIT = {
#    'user_edit':{
        #'name': 'user',
        #'endpoint':'user_edit',
        #'model': Hifuser,
        #'template_name':'platform/edit.html',
        #'permission': permissions['admin'],
        #'nextid':'uid',
        #'fields':['id','email','password','nickname','create_time','last_login','roles','avatar'],
        #'field_args':{
                #'nickname': {'widget': widgets.TextInput()},
                #'password': {'widget': widgets.TextInput()},
                #'roles': {'choices': [(val,label) for val, label in ROLE.items()],'widget': widgets.CheckboxInput()},
                #},
    #},
    'news_edit':{
        'name': 'news',
        'endpoint':'news_edit',
        'model': Hifnews,
        'template_name':'platform/edit.html',
        'nextid':'newsid',
        'permission': permissions['news'],
        'fields':['id','title','author','thumbnail','create_time','status','isbanner','content'],
        'field_args':{
                'title': {'widget': widgets.TextInput()},
                },
    },
    'activity_edit':{
        'name': 'activity',
        'endpoint':'activity_edit',
        'model': Hifactivity,
        'template_name':'platform/edit.html',
        'permission': permissions['activity'],
        'nextid':'activityid',
        'fields':['id','title','author','place','start_time','end_time','create_time','thumbnail','content'],
        'field_args':{
                'title': {'widget': widgets.TextInput()},
                'place': {'widget': widgets.TextInput()},
                },
    },
    'grapevine_edit':{
        'name': 'grapevine',
        'endpoint':'grapevine_edit',
        'model': Hifgrapevine,
        'template_name':'platform/edit.html',
        'permission': permissions['grapevine'],
        'nextid':'grapevineid',
        'fields':['id','title','author','create_time','thumbnail','content'],
        'field_args':{
                'title': {'widget': widgets.TextInput()},
                },
    },

    'lecture_edit':{
        'name': 'lecture',
        'endpoint':'lecture_edit',
        'model': Hiflecture,
        'template_name':'platform/edit.html',
        'nextid':'lectureid',
        'permission': permissions['lecture'],
        'fields':['id','title','author','thumbnail','person','place','start_time','end_time','create_time','content'],
        'field_args':{
                'title': {'widget': widgets.TextInput()},
                'person':{'widget': widgets.TextInput()},
                'place':{'widget': widgets.TextInput()},
        },
    },
    'job_edit':{
        'name': 'job',
        'endpoint':'job_edit',
        'model': Hifjob,
        'template_name':'platform/edit.html',
        'nextid':'jobid',
        'permission': permissions['job'],
        'fields':['id','title','author','thumbnail','create_time','content'],
        'field_args':{
                'title': {'widget': widgets.TextInput()},
        },
    },


    'weekperson_edit':{
        'name': 'weekperson',
        'endpoint':'weekperson_edit',
        'model': Hifweekperson,
        'template_name':'platform/edit.html',
        'permission': permissions['weekperson'],
        'nextid':'personid',
        'fields':['id','time','person_name','title','proverbes','create_time','content','thumbnail1','thumbnail2'],
        'field_args':{
                'person_name': {'widget': widgets.TextInput()},
                'title': {'widget': widgets.TextInput()},
                'proverbes': {'widget': widgets.TextInput()},
                },
    },
}

Forms = {}
for k in EDIT:
    Forms[EDIT[k]['name']] = model_form(EDIT[k]['model'],only=EDIT[k]['fields'],field_args = EDIT[k]['field_args'])

class EditView(PlatformView):
    def __init__(self, template_name):
        self.template_name = template_name

    def get_template_name(self):
        return self.template_name

    def get_model(self):
        return self.model

    def get(self,*args,**kwargs):
        if not current_user or not current_user.is_authenticated():
            return redirect(url_for(".login"))
        if 'permission' in kwargs['args']:
            check_permission(kwargs['args']['permission'])
        if 'model' in kwargs['args']:
            self.model = kwargs['args']['model']
        context = {'form': self.get_objects(*args, **kwargs)}
        if not 'fields' in kwargs['args']:
            kwargs['args']['fields'] = self.get_model()._fields.keys()
        context.update(kwargs)
        return self.render_template(context)

    def get_objects(self, *args, **kwargs):
        if not 'fields' in kwargs['args']:
            kwargs['args']['fields'] = self.get_model()._fields.keys()
        if 'id' in kwargs:
            obj = self.get_model().objects.get_or_404(id=kwargs['id'])
            form =  Forms[kwargs['args']['name']](obj=obj)
            if kwargs['args']['name'] == 'user':
                form.password.data = ''
            return form
        else:
            obj = self.get_model()()
            obj.id = Id.get_next_id(kwargs['args']['nextid'])
            form = Forms[kwargs['args']['name']](obj=obj)
            form.create_time.data=datetime.datetime.now()
            if kwargs['args']['name'] == 'user':
                form.password.data = ''
            return form

    def post(self, *args, **kwargs):
        name = request.form['name']
        form = Forms[name](request.form)
        if form.validate():
            image = None
            if 'thumbnail' in request.files:
                image = ['thumbnail']
                f = [form.thumbnail]
            if 'image1' in request.files:
                image = ['image1','image2']
                f = [form.thumbnail1,form.thumbnail2]
            if image:
                for k,i in enumerate(image):
                    try:
                        imageid = save_img(i)
                        if imageid!=0:
                            f[k].data = imageid
                    except:
                        traceback.print_exc()
                        errors = u"上传图像失败,请重试"
                        if 'password' in request.form:
                            form.password.data = ''
                        context = {
                            'form': form,
                            'args': EDIT['%s_edit' % name],
                            'errors': errors
                        }
                        return self.render_template(context)
            form.save()
            print form
            return redirect(url_for(".%s_list" % name))
        context = {
            'form': form,
            'args': EDIT['%s_edit' % name]
        }
        return self.render_template(context)

MODEL = {
    'user':Hifuser,
    'news':Hifnews,
    'activity':Hifactivity,
    'person':Hifweekperson,
    'grapevane':Hifgrapevine,
    'lecture':Hiflecture,
}
def save_img(field):
    f = request.files[field]
    if f:
        path = app.config['THUMBNAIL_PATH']
        try:
            imageid = Id.get_next_id("imageid")
            name = "%s/%s.png" % (path,imageid)
            f.save(name)
            import Image
            outfile = ["%s/%s_small.png" % (path,imageid),
            "%s/%s_mid.png" % (path,imageid),
            "%s/%s_normal.png" % (path,imageid)]
            size = [(50,50),(100,100),(150,150)]
            if field == 'image1':
                size = [(150,150),(200,200),(250,250)]
            for i in range(3):
                im = Image.open(name)
                im.thumbnail(size[i],Image.ANTIALIAS)
                im.save(outfile[i], "PNG")
        except:
            traceback.print_exc()
            raise Exception()
        return imageid
    return 0

def add_edit_views(args):
    for item in args:
        view = EditView.as_view(
                args[item]['endpoint'],
                template_name = args[item]['template_name'])
        # view = user_required(view,args[item]['permission'])
        bp_platform.add_url_rule(
                "/%s/edit/<int:id>/" % args[item]['name'],
                defaults={"args":args[item]},
                view_func=view,
                methods=['GET','POST'])
        bp_platform.add_url_rule(
                "/%s/edit/" % args[item]['name'],
                defaults={"args":args[item]},
                view_func=view,
                methods=['GET','POST'])
#add_edit_views(EDIT)
