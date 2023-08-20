import os
from pathlib import Path
from flask import send_from_directory
from flask_login import (
    login_user, current_user, 
    logout_user, login_required)
from flask.views import View


from ReadWeld.utils import if_sensor_not_exist_404, WorkingWithFileDatabase


class DownloadFileAPI(View, WorkingWithFileDatabase):
    
    methods = ['GET']
    
    decorators = [if_sensor_not_exist_404, login_required]
    
    def dispatch_request(self, mac_address: str, file_name: str):
        path = Path(self.PATH_TO_FILES_WITH_SENSORS).joinpath(mac_address)
        return send_from_directory(directory=path, filename=file_name)
