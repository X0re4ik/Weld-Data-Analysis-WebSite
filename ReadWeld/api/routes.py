from ReadWeld.api import api

from ReadWeld.api.controllers import (DownloadFileAPI,)


VERSION = 1 

PATH_TEMPLATE = f"/api/v{VERSION}"

api.add_url_rule(PATH_TEMPLATE + "/download/file/<string:mac_address>/<string:file_name>", 
                     view_func=DownloadFileAPI.as_view("show-sensors"))

