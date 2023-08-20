



from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'users.login_master'

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


from pathlib import Path 
READ_WELD_WORKDIR = Path('.').parent.absolute()


from ReadWeld.config import NAME_DB_WITH_FILES 
from ReadWeld.utils import WorkingWithFileDatabase
WorkingWithFileDatabase.NAME = NAME_DB_WITH_FILES
from ReadWeld.utils import jinja_helper
from ReadWeld.models import InitDataBase
from ReadWeld.config import Config, TestConfig

from flask import Flask
class AppCreator:
    
    app = Flask(__name__)
    
    
    def attach_config(self):
        self.__class__.app.config.from_object(Config)
        return self

    def attach_apps(self):
        db.init_app(self.__class__.app)
        login_manager.init_app(self.__class__.app)
        jinja_helper.init_app(self.__class__.app)
        return self
    
    def attach_context(self):
        self.__class__.app.app_context().push()
        with self.__class__.app.app_context():
            db.create_all()
        InitDataBase()
        return self
    
    def attach_blueprints(self):
        from ReadWeld.users.routes import users
        self.__class__.app.register_blueprint(users)
        
        from ReadWeld.sensors.routes import sensors
        self.__class__.app.register_blueprint(sensors)
        
        from ReadWeld.api.routes import api
        self.__class__.app.register_blueprint(api)
        return self
        
    @staticmethod
    def get():
        """
           Блюпринт только после контекста
        """
        app_creator = AppCreator()
        for key in AppCreator.__dict__:
            att = getattr(AppCreator, key)
            if key.startswith('attach_') and callable(att) and hasattr(att, '__call__'):
               att(app_creator) 
            
        return app_creator.app
        
                
        
app = AppCreator.get()





from werkzeug.exceptions import HTTPException


from flask import render_template

@app.errorhandler(404)
def not_found_error(error_content):
    return render_template('404.html', error_content=error_content)


# @app.errorhandler(Exception)
# def handle_exception(error):
#     if isinstance(error, HTTPException):
#         return error
    
#     return render_template("error.html", error_description=error), 500