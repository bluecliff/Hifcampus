#!/usr/bin/env python
# encoding: utf-8

from flask.ext.login import login_required
from flask import Blueprint,request,render_template,flash,abort

from hifcampus.models import Hifuser
from forms import UserForm

admin = Blueprint('admin',__name__,url_prefix='/admin')

@admin.route('/users')
@login_required
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
    return  render_template('admin/user.html',user=user,form=form)
