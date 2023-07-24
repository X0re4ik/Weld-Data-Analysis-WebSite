from flask import render_template, url_for, redirect, request, flash

from ReadWeld.users.forms import MasterRegistration, WelderRegistration, WelderUpdate, MasterUpdate, MasterLoginForm
from ReadWeld import db 
from ReadWeld.models import Worker, Master, Welder
from ReadWeld.users import users


from sqlalchemy import and_
from ReadWeld.users.utils import MasterLogin
from flask_login import login_user, current_user
from flask import  request, abort
from django.utils.http import url_has_allowed_host_and_scheme



@users.route("/users/<int:id>/edit", methods=['GET', 'POST'])
def edit_master(id: int):
    if current_user.get_id() != id:
        redirect(url_for("users.login_master"))
    
    master = Master.query.filter_by(id=id).first()
    worker = Worker.query.filter_by(id=master.worker_id).first()
    
    form = MasterUpdate(
        first_name=worker.first_name,
        second_name=worker.second_name,
        phone=worker.phone,
        email=master.email,
        notification=master.notification
    )
    
    if form.validate_on_submit(old_phone=worker.phone,
                               old_email=master.email):
        form.populate_obj(worker)
        form.populate_obj(master)
        db.session.commit()
    

    return render_template('users/edit/master.html',
                           form=form)