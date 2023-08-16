import os
from pathlib import Path
from flask import send_from_directory
from flask_login import (
    login_user, current_user, 
    logout_user, login_required)
from flask.views import View


from ReadWeld.utils import r_if_sensor_not_exist

PATH_TO_DB_WITH_SENSORS_FILES = Path(os.getenv("PATH_TO_DB_WITH_FILES")).joinpath("sensors")

class DownloadFileAPI(View):
    
    methods = ['GET']
    
    decorators = [r_if_sensor_not_exist, login_required]
    
    PATH_TO_DB_WITH_SENSORS_FILES: str
    
    def dispatch_request(self, mac_address: str, file_name: str):
        path = Path(self.__class__.PATH_TO_DB_WITH_SENSORS_FILES).joinpath(mac_address)
        return send_from_directory(directory=path, filename=file_name)

DownloadFileAPI.PATH_TO_DB_WITH_SENSORS_FILES = PATH_TO_DB_WITH_SENSORS_FILES
