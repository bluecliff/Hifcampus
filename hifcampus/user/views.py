#!/usr/bin/env python
# encoding: utf-8

import os
from flask import Blueprint,render_template,send_from_directory,abort,redirect,url_for,request,flash
from flask import current_app as APP
from flask.ext.login import login_required,current_user,login_user,logout_user,confirm_login,login_fresh
from hifcampus.extensions import db,login_manager
from hifcampus.models import Hifuser,Id
from forms import LoginForm,SignupForm

user = Blueprint('user',__name__)

@user.route('/')
def index():
    if current_user.is_authenticated():
        return render_template('user/index.html',user=current_user)
    else:
        return redirect(url_for('user.login'))

@user.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('user.index'))
    form = LoginForm(email=request.args.get('email',None),next=request.args.get('next',None))
    if form.validate_on_submit():
        user,authenticated=Hifuser.authenticate(form.email.data,form.password.data)
        if user and authenticated:
            remember = request.form.get('remember')=='y'
            if login_user(user,remember=remember):
                flash("Logged in",'success')
            return redirect(form.next.data or url_for('user.index'))
        else:
            flash("Invalid Login",'error')
    return render_template('user/login.html',form=form)

@user.route('/signup',methods=['GET','POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('user.index'))
    form = SignupForm(next=request.args.get('next'))
    if form.validate_on_submit():
        user = Hifuser()
        form.populate_obj(user)
#        db.session.add(user)
#        db.session.commit()
        user.id=Id.get_next_id('uid')
        user.save()
        if login_user(user):
            return redirect(form.next.data or url_for('user.index'))
    return render_template('user/signup.html',form=form)


@user.route('/<int:user_id>/profile')
def profile(user_id):
    user = Hifuser.get_by_id(user_id)
    return render_template('user/profile.html', user=user)


@user.route('/<int:user_id>/avatar/<path:filename>')
@login_required
def avatar(user_id, filename):
    dir_path = os.path.join(APP.config['UPLOAD_FOLDER'], 'user_%s' % user_id)
    return send_from_directory(dir_path, filename, as_attachment=True)