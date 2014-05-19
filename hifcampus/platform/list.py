#!/usr/bin/env python
# encoding: utf-8

from hifcampus.extensions import permissions
from hifcampus.models import Hifuser,Hiflecture,Hifnews,Hifweekperson,Hifjob,Hifactivity,Hifgrapevine
from .platform import bp_platform,PlatformView
from hifcampus.constants import DEFAULT_PERPAGE
class PageListView(PlatformView):

    def __init__(self, template_name):
        self.template_name = template_name

    def get_template_name(self):
        return self.template_name

    def get_model(self):
        return self.model

    def get_objects(self, *args, **kwargs):
        return self.get_model().objects.paginate(page=kwargs['page'], per_page=DEFAULT_PERPAGE)


LIST = {
       'news':{
        'type':PageListView,
        'name': 'news',
        'endpoint':'news_list',
        'model': Hifnews,
        'template_name':'platform/list.html',
        'permission': permissions['news'],
        'action_new': {
            'name':u'新建资讯',
            'endpoint':'news_edit',},
        'fields':['id','title','author','create_time','status'],
        'edit':'news_edit',
        'status':[u'审查中',u'通过'],
    },
    'activity':{
        'type':PageListView,
        'name': 'activity',
        'endpoint':'activity_list',
        'model': Hifactivity,
        'template_name':'platform/list.html',
        'permission': permissions['activity'],
        'action_new': {
            'name':u'新建活动',
            'endpoint':'activity_edit',},
        'fields':['id','title','author','place','start_time','create_time','status'],
        'edit':'activity_edit',
        'status':[u'审查中',u'通过'],
    },
    'grapevine':{
        'type':PageListView,
        'name': 'grapevine',
        'endpoint':'grapevine_list',
        'model': Hifgrapevine,
        'template_name':'platform/list.html',
        'permission': permissions['grapevine'],
        'action_new': {
            'name':u'新建消息',
            'endpoint':'grapevine_edit',},
        'fields':['id','title','author','create_time','status'],
        'edit':'grapevine_edit',
        'status':[u'审查中',u'通过'],
    },

    'job':{
        'type':PageListView,
        'name':'job',
        'endpoint':'job_list',
        'model':Hifjob,
        'template_name':'platform/list.html',
        'permission':permissions['job'],
        'action_new':{
            'name':u'新建招聘',
            'endpoint':'job_edit',
        },
        'fields':['id','title','author','create_time','status'],
        'edit':'job_edit',
        'status':[u'审查中',u'通过'],
    },

    'lecture':{
        'type':PageListView,
        'name':'lecture',
        'endpoint':'lecture_list',
        'model':Hiflecture,
        'template_name':'platform/list.html',
        'permission':permissions['lecture'],
        'action_new':{
            'name':u'新建讲座',
            'endpoint':'lecture_edit',
        },
        'fields':['id','title','author','place','person','start_time','create_time','status'],
        'edit':'lecture_edit',
        'status':[u'审查中',u'通过'],
    },
    'weekperson':{
        'type':PageListView,
        'name': 'weekperson',
        'endpoint':'weekperson_list',
        'model': Hifweekperson,
        'template_name':'platform/list.html',
        'permission': permissions['weekperson'],
        'action_new': {
            'name':u'新建人物',
            'endpoint':'weekperson_edit',},
        'fields':['id','person_name','title','create_time','status'],
        'edit':'weekperson_edit',
        'status':[u'审查中',u'通过'],
    },
}

def add_list_views(args):
    for item in args:
        view = args[item]['type'].as_view(
                args[item]['endpoint'],
                template_name = args[item]['template_name'])
        # view = user_required(view,args[item]['permission'])
        bp_platform.add_url_rule(
                    "/%s/list/" % args[item]['name'],
                    defaults={"page":1,"args":args[item]},
                    view_func=view,
                    methods=['GET','POST'])
        bp_platform.add_url_rule(
                    "/%s/list/<int:page>/" % args[item]['name'],
                    defaults={"args":args[item]},
                    view_func=view,
                    methods=['GET','POST'])
#add_list_views(LIST)
