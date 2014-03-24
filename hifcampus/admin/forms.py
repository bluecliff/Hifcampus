#!/usr/bin/env python
# encoding: utf-8

from hifcampus.models import Hifuser
from flask.ext.wtf import Form
from wtforms import HiddenField,SubmitField,TextField,DateField,SelectMultipleField
from flask.ext.wtf.html5 import EmailField
from wtforms.validators import Required,Email,Length
from wtforms import widgets
from hifcampus.constants import ROLE
from hifcampus.utils import USERNAME_LEN_MAX,USERNAME_LEN_MIN



class UserForm(Form):
    next=HiddenField()
#    role = RadioField(u'Role',[AnyOf([str(val) for val in ROLE.keys()])],
#            choices=[(str(val),label) for val,label in ROLE.items()])
    email = EmailField(u"Email",[Required(),Email()])
    nickname = TextField(u"User name",[Required(),Length(USERNAME_LEN_MIN,USERNAME_LEN_MAX)])
    role = SelectMultipleField(u'Role',choices=[(val,label) for val,label in ROLE.items()],option_widget=widgets.CheckboxInput(),coerce=int,widget=widgets.ListWidget(prefix_label=False))
    created_time = DateField(u'Created time')
    submit = SubmitField(u'Save')
