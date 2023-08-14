from ReadWeld.api import api

from ReadWeld.api.controllers import (ShowSensorsView,)


VERSION = 1 

PATH_TEMPLATE = f"/api/v{VERSION}"

api.add_url_rule(PATH_TEMPLATE + "/", 
                     view_func=ShowSensorsView.as_view("show-sensors"))

