
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ReadWeld.config import Config, TestConfig
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'users.login_master'

db = SQLAlchemy()


from ReadWeld.models import *
from ReadWeld.JinjaHelper import JinjaHelper


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
    
    
    
    return app
