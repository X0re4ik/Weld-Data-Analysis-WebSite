from flask import render_template, url_for, redirect, request, flash

from ReadWeld.users.forms import MasterRegistration, WelderRegistration, WelderUpdate, MasterUpdate, MasterLoginForm
from ReadWeld import db 
from ReadWeld.models import Worker, Master, Welder
from ReadWeld.users import users





class RegistrationHelper:
    
    def __init__(self, first_name: str, second_name: str, phone: str):
        self.first_name = first_name
        self.second_name = second_name
        self.phone = phone
        
        self.worker_id = self.commit_worker(self.first_name, self.second_name, self.phone)
    
    
    def commit_welder(self, category: str):
        welder = Welder(category=category, worker_id=self.worker_id)
        return self.add_and_commit_in_db(welder)
    
    def commit_master(self,
                      email: str,
                      password: str,
                      notification: bool) -> int:
        master = Master(
            email=email,
            password=password,
            notification=notification,
            worker_id=self.worker_id
        )
        return self.add_and_commit_in_db(master)
    
    

    
    @staticmethod
    def add_master_from_form(form):
        return RegistrationHelper(
            first_name=form.first_name.data,
            second_name=form.second_name.data,
            phone=form.phone.data).commit_master(
                email=form.email.data,
                password=form.password.data,
                notification=form.notification.data
            )
            
    @staticmethod
    def add_welder_from_form(form):
        return RegistrationHelper(
            first_name=form.first_name.data,
            second_name=form.second_name.data,
            phone=form.phone.data).commit_welder(
                category=form.category.data)
    
    
    @staticmethod
    def get_list_of_masters():
        list_of_masters = Master.query.filter_by().all()  
        workers = [ Worker.query.filter_by(id=master.worker_id).first() for master in list_of_masters ]
        return list(zip(workers, list_of_masters))
    
    @staticmethod
    def get_list_of_welders():
        list_of_welders = Welder.query.filter_by().all()  
        workers = [ Worker.query.filter_by(id=master.worker_id).first() for master in list_of_welders ]
        return list(zip(workers, list_of_welders))
        
    
    @staticmethod
    def commit_worker(first_name: str, second_name: str, phone: str) -> int:
        worker = Worker(
            first_name=first_name,
            second_name=second_name,
            phone=phone)
        return RegistrationHelper.add_and_commit_in_db(worker)
    
    
    @staticmethod
    def add_and_commit_in_db(row) -> int:
        db.session.add(row)
        db.session.commit()
        return row.id
    
@users.route("/welder/add", methods=['GET', 'POST'])
def add_welder():
    form = WelderRegistration()
    if form.validate_on_submit():
        RegistrationHelper.add_welder_from_form(form)
        return redirect(url_for('users.add_welder'))
    
    return render_template('users/add/add.html', form=form)


from flask_login import login_required, current_user





@users.route("/users/welders", methods=['GET', 'POST'])
def show_welders():

    welders = Welder.query.filter_by().all()
    workers = [Worker.query.filter_by(id=welder.worker_id).first() for welder in welders ]
    performances = [list(worker.calculate_performance()) for worker in workers]
    
    welders = [welder.to_dict() for welder in welders]
    
    return render_template("users/show/show.html",
                           welders=welders, 
                           performances=performances,
                           masterID=current_user.get_id())



@users.route("/users/welder/<int:id>/edit", methods=['GET', 'POST'])
def edit_welder(id: int):
    
    welder = Welder.query.filter_by(id=id).first()
    worker = Worker.query.filter_by(id=welder.worker_id).first()
    
    form = WelderUpdate(
        first_name=worker.first_name,
        second_name=worker.second_name,
        phone=worker.phone,
        category=welder.category)
    
    if form.validate_on_submit(old_phone=worker.phone):
        form.populate_obj(worker)
        form.populate_obj(welder)
        db.session.commit()
      
    return render_template(
        'users/edit/edit.html',
        form=form,
        welder=welder.to_dict(),
        performances=[list(worker.calculate_performance())])






from sqlalchemy import and_
from ReadWeld.users.utils import MasterLogin
from flask_login import login_user
from flask import  request, abort
from django.utils.http import url_has_allowed_host_and_scheme




from flask.views import View

class MasterLoginView(View):
    methods = ["POST", "GET"]

    def dispatch_request(self):
        if current_user.is_authenticated:
            return redirect(url_for('users.show_welders'))
    
        form = MasterLoginForm()
        
        if form.validate_on_submit():
            phone = form.phone.data
            
            master = Master.exist(phone)
            if master and master.password == form.password.data:
                master_login = MasterLogin().fromDB(master.worker_id)
                login_user(master_login, remember=form.remember_me.data)
                next = request.args.get('next')
                if not url_has_allowed_host_and_scheme(next, request.host):
                    return abort(400)
                return redirect(next or url_for('users.login_master'))
        return render_template("/users/login_master.html", form=form)


users.add_url_rule("/users/login", 
                     view_func=MasterLoginView.as_view("login_master"))

class MasterEditView(View):
    
    methods = ["POST", "GET"]
    
    
    def __init__(self) -> None:
        self.template = "/".join(
            ("users", "edit", "master.html")
        )
    
    def dispatch_request(self, id: int):
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
        

        return render_template(
                self.template,
                form=form,
                masterID=current_user.get_id())

users.add_url_rule("/users/<int:id>/edit", 
                     view_func=MasterEditView.as_view("edit_master")
                     )




