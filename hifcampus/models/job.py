#!/usr/bin/env python
# encoding: utf-8

from hifcampus.extensions import db
from hifcampus.models import Hifuser,Hifcomment
import datetime
import json
from mongoengine.queryset import queryset_manager

class Hifjob(db.Document):
    """Jobs model"""
    id = db.IntField(primary_key=True,verbose_name=u"ID")
    title = db.StringField(verbose_name=u"招聘标题",unique=True)
    author = db.ReferenceField(Hifuser,verbose_name=u"来源")
    content = db.StringField(verbose_name=u"招聘内容")
    comments = db.ListField(db.ReferenceField(Hifcomment))
    create_time = db.DateTimeField(default=datetime.datetime.utcnow(),verbose_name=u"创建时间")
    status=db.IntField(default=1,verbose_name=u"状态")
    isbanner=db.IntField(default=0)
    thumbnail = db.IntField(default=4)
    #category = db.StringField(default=u"招聘",verbose_name=u"信息来源")
    #自定义查询方法
    @queryset_manager
    def getlist(doc_cls, queryset, postid, perpage):
        '''
        查询工作列表
        '''
        if postid==0:
            res = queryset.filter(status=1).exclude('content').exclude('comments').exclude('status').exclude('isbanner')[0:perpage]
        else:
            res = queryset.filter(status=1,id__lt=postid).exclude('content').exclude('comments').exclude('status').exclude('isbanner')[0:perpage]
        reslist = json.loads(res.to_json())
        for i,item in enumerate(res):
            try:
                reslist[i]['author_name'] = item.author.nickname
                reslist[i]['author_thumbnail'] = item.author.thumbnail
            except:
                reslist[i]['author_name'] = ""
                reslist[i]['author_thumbnail'] = ""
        return reslist

    @queryset_manager
    def getcontent(doc_cls,queryset,postid):
        '''
        查询工作具体信息
        '''
        try:
            res = queryset.get(status=1,id=postid)#.only('comments')
        except:
            return None
        return {'comments':res['comments'],'content':res['content']}

    meta = {
            'ordering':['-id'],
            }
