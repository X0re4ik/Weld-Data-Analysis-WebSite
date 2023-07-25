from ReadWeld.users import users

from ReadWeld.users.controllers import (
    WelderAddView, WeldersShowView,
    WelderEditView, MasterLoginView,
    MasterEditView
)

users.add_url_rule("/users/welder/add", 
                     view_func=WelderAddView.as_view("add_welder"))

users.add_url_rule("/users/welders", 
                     view_func=WeldersShowView.as_view("show_welders"))

users.add_url_rule("/users/welder/<int:id>/edit", 
                     view_func=WelderEditView.as_view("edit_welder"))

users.add_url_rule("/users/login", 
                     view_func=MasterLoginView.as_view("login_master"))

users.add_url_rule("/users/<int:id>/edit", 
                     view_func=MasterEditView.as_view("edit_master"))