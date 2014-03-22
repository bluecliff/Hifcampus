#!/usr/bin/env python
# encoding: utf-8

from hifcampus.models import Hifuser
from flask.ext.wtf import Form
from wtforms import HiddenField,SubmitField,RadioField,DateField
from wtforms.validators import Required,AnyOf
from hifcampus.constants import ROLE

class UserForm(Form):
    next=HiddenField()
    role = RadioField(u'Role',[AnyOf([str(val) for val in ROLE.keys()])],
            choices=[(str(val),label) for val,label in ROLE.items()])
    created_time = DateField(u'Created time')
    submit = SubmitField(u'Save')
