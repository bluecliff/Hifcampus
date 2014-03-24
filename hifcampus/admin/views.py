#!/usr/bin/env python
# encoding: utf-8

from flask.ext.login import login_required
from flask import Blueprint,request,render_template,flash,abort,url_for,redirect
from hifcampus.models import Hifuser
from forms import UserForm
from flask.ext.principal import Permission,RoleNeed
admin = Blueprint('admin',__name__,url_prefix='/admin')
admin_permission = Permission(RoleNeed('admin'))
@admin.route('/users')
@login_required
#@admin_permission.require()
def users():
    users = Hifuser.objects.all()
    return render_template('admin/users.html',users=users)

@admin.route('/user/<int:user_id>',methods=['GET','POST'])
@login_required
def user(user_id):
    user = Hifuser.objects(id=user_id).first()
    if user is None:
        abort(404)
    form = UserForm(obj=user,next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)
        user.save()
        flash("User updated.","success")
        return redirect(form.next.data or url_for('admin.users'))
    return  render_template('admin/user.html',user=user,form=form)

@admin.route('/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    user = Hifuser.objects(id=user_id).first()
    if user is None:
        abort(404)
    user.delete()
    return redirect(url_for('admin.users'))
