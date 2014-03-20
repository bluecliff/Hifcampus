#!/usr/bin/env python
# encoding: utf-8

from hifcampus import db
from hifcampus.models import Hifuser,Hifcomment
import datetime
import json
from mongoengine.queryset import queryset_manager

class Hiflecture(db.Document):
    """Lecture model"""
    id = db.IntField(primary_key=True,verbose_name=u"ID")
    title = db.StringField(verbose_name=u"标题",unique=True)
    author = db.ReferenceField(Hifuser,verbose_name=u"来源")
    content = db.StringField(verbose_name=u"内容")
    comments = db.ListField(db.ReferenceField(Hifcomment))
    place = db.StringField(verbose_name=u"地点")
    person = db.StringField(verbose_name=u"主讲人")
    start_time = db.DateTimeField(verbose_name=u"开始时间")
    end_time = db.DateTimeField(verbose_name=u"结束时间")
    attend = db.ListField(db.ReferenceField(Hifuser))
    create_time = db.DateTimeField(default=datetime.datetime.utcnow(),verbose_name=u"创建时间")
    thumbnail = db.IntField(default=3)
    #默认为0状态，待审核
    status = db.IntField(default=1,verbose_name=u"状态")
    isbanner = db.IntField(default=0)
    #自定义查询方法
    @queryset_manager
    def getlist(doc_cls,queryset,postid,perpage):
        '''
        查询讲座列表
        '''
        if postid==0:
            res = queryset.filter(status=1).exclude('content').exclude('comments').exclude('status').exclude('isbanner')[0:perpage]
        else:
            res = queryset.filter(status=1,id__lt=postid).exclude('content').exclude('comments').exclude('status').exclude('isbanner')[0:perpage]
        reslist = json.loads(res.to_json())
        for i,item in enumerate(res):
            reslist[i]['author_name'] = item.author.nickname
            reslist[i]['author_thumbnail'] = item.author.thumbnail
        return reslist
    @queryset_manager
    def getcontent(doc_cls,queryset,postid):
        '''
        查询讲座具体信息
        '''
        try:
            res = queryset.get(status=1,id=postid)#.only('comments')
        except:
            return None
        return {'comments':res['comments'],'content':res['content']}


    meta = {
        'ordering': ['-id'],
    }
