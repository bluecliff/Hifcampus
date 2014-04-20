#!/usr/bin/env python
# encoding: utf-8

from flask.ext.login import login_required,current_user,login_user,logout_user
from flask import Blueprint,request,render_template,flash,abort,url_for,redirect,session,current_app as APP
from hifcampus.models import Hifuser,Id
from forms import UserForm,LoginForm,SignupForm
from flask.ext.principal import Permission,RoleNeed,identity_changed,AnonymousIdentity,Identity
from werkzeug import generate_password_hash

bp_user= Blueprint('bp_user',__name__,template_folder='templates',url_prefix='/user')
admin_permission = Permission(RoleNeed('admin'))

@bp_user.route('/users/')
@login_required
@admin_permission.require(403)
def users():
    users = Hifuser.objects.all()
    return render_template('user/users.html',users=users)

@bp_user.route('/user/<int:user_id>/',methods=['GET','POST'])
@login_required
@admin_permission.require(403)
def user(user_id):
    user = Hifuser.objects(id=user_id).first()
    if user is None:
        abort(404)
    form = UserForm(obj=user,next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)
        user.save()
        flash("User updated.","success")
        return redirect(form.next.data or url_for('.users'))
    print user
    print form
    return  render_template('user/user.html',user=user,form=form)

@bp_user.route('/delete/<int:user_id>/')
@login_required
@admin_permission.require(403)
def delete_user(user_id):
    user = Hifuser.objects(id=user_id).first()
    if user is None:
        abort(404)
    user.delete()
    return redirect(url_for('.users'))

@bp_user.route('/login/',methods=['GET','POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('bp_user.users'))
    form = LoginForm(email=request.args.get('email',None),next=request.args.get('next',None))
    if form.validate_on_submit():
        user,authenticated=Hifuser.authenticate(form.email.data,form.password.data)
        if user and authenticated:
            remember = request.form.get('remember')=='y'
            if login_user(user,remember=remember):
                identity_changed.send(APP._get_current_object(),identity=Identity(user.id))
                flash("Logged in",'success')
            return redirect(form.next.data or url_for('bp_platform.index'))
        else:
            flash("Invalid Login",'error')
    return render_template('user/login.html',form=form)
@bp_user.route('/logout/',methods=['GET'])
def logout():
    if current_user.is_authenticated():
        logout_user()
        for key in ('identity.name','identity.auth_type'):
            session.pop(key,None)
        identity_changed.send(APP._get_current_object(),identity=AnonymousIdentity())
        flash('logout success')
    return redirect(url_for('bp_user.login'))
@bp_user.route('/signup/',methods=['GET','POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('bp_platform.index'))
    form = SignupForm(next=request.args.get('next'))
    if form.validate_on_submit():
        user = Hifuser()
        form.populate_obj(user)
        user.password=generate_password_hash(user.password)
        user.id=Id.get_next_id('uid')
        user.save()
        if login_user(user):
            return redirect(form.next.data or url_for('bp_user.users'))
    return render_template('user/signup.html',form=form)
