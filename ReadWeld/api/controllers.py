from pathlib import Path
from flask import send_from_directory
from flask_login import (
    login_user, current_user, 
    logout_user, login_required)
from flask.views import View


from ReadWeld.api import api

class DownloadFileAPI(View):
    
    methods = ['POST', 'GET']
    
    PATH_TO_DB_WITH_FILES = r"C:\Users\Ferre\OneDrive\Документы\Xore4ik\ZIT-ReadWeld\db\sensors"
    
    def dispatch_request(self, mac_address: str, file_name: str):
        path = Path(self.__class__.PATH_TO_DB_WITH_FILES).joinpath(mac_address)
        return send_from_directory(directory=path, filename=file_name)
