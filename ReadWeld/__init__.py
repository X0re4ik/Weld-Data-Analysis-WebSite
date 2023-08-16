from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'users.login_master'

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


import os
from dotenv import load_dotenv
from ReadWeld.utils import envNotFound

DOTENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(DOTENV_PATH): load_dotenv(DOTENV_PATH)
else: raise envNotFound(DOTENV_PATH)


from flask import Flask
class AppCreator:
    
    app = Flask(__name__)
    
    PATH_TO_DB_WITH_FILES: str = os.getenv("PATH_TO_DB_WITH_FILES")
    
    def include_config(self):
        from ReadWeld.config import Config, TestConfig
        self.__class__.app.config.from_object(Config)
        return self
    
    def include_blueprints(self):
        from ReadWeld.users.routes import users
        self.__class__.app.register_blueprint(users)
        
        from ReadWeld.sensors.routes import sensors
        self.__class__.app.register_blueprint(sensors)
        
        from ReadWeld.api.routes import api
        self.__class__.app.register_blueprint(api)
        return self
    
    def include_context(self):
        self.__class__.app.app_context().push()
        with self.__class__.app.app_context():
            from ReadWeld.models import InitDataBase
            InitDataBase()
            db.create_all()
        return self
        
    def init_apps(self):
        db.init_app(self.__class__.app)
        login_manager.init_app(self.__class__.app)
        return self
    
    def include_other(self):
        from ReadWeld.JinjaHelper import JinjaHelper
        JinjaHelper.load(self.__class__.app)
        return self
    
    def create_pantry(self):
        self._create_pantry(self.__class__.PATH_TO_DB_WITH_FILES)
        return self

    @staticmethod
    def _create_pantry(path):
        from pathlib import Path
        path_ = Path(path)
        path_.mkdir(exist_ok=True)
        
        needed_dirs = ["sensors"]
        
        for needed_dir in needed_dirs:
            child_dir = path_.joinpath(needed_dir)
            child_dir.mkdir(exist_ok=True)
        
        
        
    
    @staticmethod
    def get_app():
        """
           Блюпринт только после контекста
        """
        
        return AppCreator()             \
                .include_config()       \
                .init_apps()            \
                .include_context()      \
                .include_blueprints()   \
                .include_other()        \
                .create_pantry()        \
                .app
        
                
        
app = AppCreator.get_app()
        


from werkzeug.exceptions import HTTPException



# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('error.html', error_description=error, error_code=404), 404


# @app.errorhandler(Exception)
# def handle_exception(error):
#     if isinstance(error, HTTPException):
#         return error
    
#     return render_template("error.html", error_description=error), 500