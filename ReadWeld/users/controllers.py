from flask import render_template, url_for, redirect, request, abort
from flask.views import View
from flask_login import login_user, login_required, current_user
from django.utils.http import url_has_allowed_host_and_scheme


from ReadWeld import db
from ReadWeld.models import Worker, Master, Welder
from ReadWeld.utils import if_welder_not_exist_404

from ReadWeld.users.utils import MasterLogin
from ReadWeld.users.forms import WelderRegistration, WelderUpdate, MasterUpdate, MasterLoginForm


class WelderAddView(View):
    
    methods=['GET', 'POST']
    
    decorators = [login_required]
    
    def __init__(self) -> None:
        self.template = "/".join(
            ("users", "add", "add.html")
        )
    
    def dispatch_request(self):
        form = WelderRegistration()
        if form.validate_on_submit():
            first_name  =   form.first_name.data
            second_name =   form.second_name.data
            phone       =   form.phone.data
            category    =   form.category.data
            
            worker = Worker(first_name=first_name, second_name=second_name, phone=phone)
            db.session.add(worker)
            db.session.commit()
            
            welder = Welder(category=category, worker_id=worker.id)
            db.session.add(welder)
            db.session.commit()
            
            return redirect(url_for('users.add_welder'))
        return render_template(self.template, form=form, masterID=current_user.get_id())

class WeldersShowView(View):
    
    methods=['GET']
    
    decorators = [login_required]
    
    def __init__(self) -> None:
        self.template = "/".join(
            ("users", "show", "show.html")
        )
    
    def dispatch_request(self):
        welders = Welder.query.filter_by().all()
        workers = [Worker.query.filter_by(id=welder.worker_id).first() for welder in welders ]
        performances = [list(worker.calculate_performance()) for worker in workers]
        
        welders = [welder.to_dict() for welder in welders]
        
        return render_template(self.template,
                            welders=welders, 
                            performances=performances,
                            masterID=current_user.get_id())


class WelderEditView(View):
    
    methods=['GET', 'POST']
    
    decorators = [login_required, if_welder_not_exist_404]
    
    def __init__(self) -> None:
        self.template = "/".join(
            ("users", "edit", "edit.html")
        )
    
    def dispatch_request(self, id: int):
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
            self.template,
            form=form,
            welder=welder.to_dict(),
            performances=[list(worker.calculate_performance())], masterID=current_user.get_id())
    

class MasterLoginView(View):
    
    methods = ["POST", "GET"]

    def __init__(self) -> None:
        self.template = "/".join(
            ("users", "login_master.html")
        )
        
    
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
                return redirect(url_for('users.login_master'))
                # next = request.args.get('next')
                # if not url_has_allowed_host_and_scheme(next, request.host):
                #     return abort(400)
                # return redirect(next or url_for('users.login_master'))
            
        return render_template(self.template, form=form, masterID=current_user.get_id())


class MasterEditView(View):
    
    methods = ["POST", "GET"]
    
    decorators = [login_required]
    
    
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
