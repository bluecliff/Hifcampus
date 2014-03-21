#!/usr/bin/env python
# encoding: utf-8

from hifcampus.extensions import db

from user import Hifuser
from comment import Hifcomment
import datetime
import json
from mongoengine.queryset import queryset_manager


class Hifweekperson(db.Document):
    """weekperson model"""
    id = db.IntField(primary_key=True,verbose_name=u"ID")
    person_name = db.StringField(verbose_name=u"姓名")
    title = db.StringField(verbose_name=u"职位、成就、副标题")
    proverbes = db.StringField(verbose_name=u"寄语")
    content = db.StringField(verbose_name=u"内容")
    create_time = db.DateTimeField(default=datetime.datetime.utcnow(),verbose_name=u"创建时间")
    description = db.StringField(verbose_name=u"简短描述，第几期等")
    thumbnail1 = db.IntField(default=3)
    thumbnail2 = db.IntField(default=0)
    status = db.IntField(default=1,verbose_name=u"状态")
    time = db.IntField(default=1,min_value=1,verbose_name=u'第几期')
    #自定义查询方法
    @queryset_manager
    def getlist(doc_cls,queryset,postid,perpage):
        '''
        查询列表
        '''
        if postid==0:
            res = queryset.filter(status=1).exclude('content').exclude('status')[0:perpage]
        else:
            res = queryset.filter(status=1,id__lt=postid).exclude('status')[0:perpage]
        reslist = json.loads(res.to_json())
        return reslist
    @queryset_manager
    def getcontent(doc_cls,queryset,postid):
        '''
        内容查询
        '''
        try:
            res = queryset.get(status=1,id=postid)#.only('comments')
        except:
            return None
        return {'content':res['content']}


    meta = {
        'ordering': ['-id'],
    }
