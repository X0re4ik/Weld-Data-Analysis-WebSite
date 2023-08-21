from pathlib import Path
READ_WELD_WORKDIR = Path('.').parent.absolute() #Рабочая директория для web-приложения

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from werkzeug.exceptions import HTTPException

from ReadWeld.config import NAME_DB_WITH_FILES, Config, TestConfig
from ReadWeld.utils import WorkingWithFileDatabase, jinja_helper, FillDBWithStandardValues

WorkingWithFileDatabase.NAME = NAME_DB_WITH_FILES   # Название папки для хранения файлов в файловой системе
                                                    # - <NAME>
                                                    # - web
                                                    #   - ReadWeld
                                                    #   - run.py

login_manager = LoginManager()
login_manager.login_view = 'users.login_master'


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
        return self
    
    def attach_blueprints(self):
        from ReadWeld.users.routes import users
        self.__class__.app.register_blueprint(users)
        
        from ReadWeld.sensors.routes import sensors
        self.__class__.app.register_blueprint(sensors)
        
        from ReadWeld.api.routes import api
        self.__class__.app.register_blueprint(api)
        return self
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AppCreator, cls).__new__(cls)
        return cls.instance
    
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

FillDBWithStandardValues.fill()

@app.errorhandler(404)
def not_found_error(error_content):
    return render_template('errors/404.html', error_content=error_content)


@app.errorhandler(Exception)
def handle_exception(error_content):
    if isinstance(error_content, HTTPException):
        return redirect(url_for('not_found_error', error_content=error_content))
    
    return render_template("errors/500.html", error_content=error_content), 500