#!/usr/bin/env python
# encoding: utf-8

from flask.ext.wtf import Form
from wtforms import ValidationError,HiddenField,BooleanField,TextField,PasswordField,SubmitField
from wtforms.validators import Required,Length,EqualTo,Email
from flask.ext.wtf.html5 import EmailField
from hifcampus.models import Hifuser
from hifcampus.utils import PASSWORD_LEN_MAX,PASSWORD_LEN_MIN,USERNAME_LEN_MAX,USERNAME_LEN_MIN

class LoginForm(Form):
    next = HiddenField()
    email = TextField(u"E-mail",[Required()])
    password = PasswordField(u"Password",[Required()])
    remember = BooleanField(u"Remember me")
    submit = SubmitField(u"Signin")

class SignupForm(Form):
    next = HiddenField()
    email = EmailField(u"Email",[Required(),Email()])
    password=PasswordField(u"Password",[Required(),Length(PASSWORD_LEN_MIN,PASSWORD_LEN_MAX)])
    password_second=PasswordField(u"Repeat Password",[Required(),EqualTo('password')])
    nickname = TextField(u"User name",[Required(),Length(USERNAME_LEN_MIN,USERNAME_LEN_MAX)])
    submit = SubmitField(u"Signup")

    def validate_nickname(self,field):
        if Hifuser.objects(nickname=field.data).first() is not None:
            raise ValidationError(u'this username has is taken')
    def validate_email(self,field):
        if Hifuser.objects(email=field.data).first() is not None:
            raise ValidationError(u'this email is taken')

