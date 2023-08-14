
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ReadWeld.config import Config, TestConfig
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'users.login_master'

db = SQLAlchemy()


from ReadWeld.models import *
from ReadWeld.JinjaHelper import JinjaHelper

from flask import render_template
def create_app():
    print(__name__)
    app = Flask(__name__)
    
    JinjaHelper.load(app)
    
    app.config.from_object(TestConfig)
    db.init_app(app)
    login_manager.init_app(app)
    
    app.app_context().push()
    with app.app_context(): db.create_all()
        
    InitDataBase()
    
    from ReadWeld.users.routes import users
    app.register_blueprint(users)
    
    from ReadWeld.sensors.routes import sensors
    app.register_blueprint(sensors)
    
    from ReadWeld.api.routes import api
    app.register_blueprint(api)

    
    return app


app = create_app()


from werkzeug.exceptions import HTTPException



# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('error.html', error_description=error, error_code=404), 404


# @app.errorhandler(Exception)
# def handle_exception(error):
#     if isinstance(error, HTTPException):
#         return error
    
#     return render_template("error.html", error_description=error), 500