#!/usr/bin/env python
# encoding: utf-8
import json
from id import Id
from user import Hifuser
from comment import Hifcomment
from news import Hifnews
from activity import Hifactivity
from weekperson import Hifweekperson
from lecture import Hiflecture
from job import Hifjob
from grapevine import Hifgrapevine


Model={
        'news':Hifnews,
        'activity':Hifactivity,
        'job':Hifjob,
        'lecture':Hiflecture,
        'user':Hifuser,
        'grapevine':Hifgrapevine,
        'weekperson':Hifweekperson,
        'comment':Hifcomment,
    }

#增加评论信息
def add_comment(model_name,postid,data):
    comment=Hifcomment();
    comment.id=Id.get_next_id('commentid')
    comment.content = data['content']
    comment.author=Hifuser.objects.get(id=int(data['author_id']))
    comment.save()
    model = Model[model_name].objects.get(id=int(postid))
    model.comments.append(comment)
    model.save()
    return True

#查询某一条发布及其对应的评论列表
def get_detail(model_name,postid):
    exlude_fields=['isbanner','status']
    item = Model[model_name].objects.filter(id=int(postid)).exclude(*exlude_fields)
    res=json.loads(item.to_json())
    if len(res)==0:
        return None
    else:
        for key in res[0].keys():
            if key in exlude_fields:
                res.pop(key)
    return res[0]

