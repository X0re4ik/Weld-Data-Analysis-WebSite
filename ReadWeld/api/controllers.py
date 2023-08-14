from datetime import datetime
from abc import ABC

from flask import render_template, url_for, redirect, request
from flask_login import (
    login_user, current_user, 
    logout_user, login_required)
from flask.views import View


from ReadWeld.sensors.forms import SensorForm
from ReadWeld import db
from ReadWeld.models import Sensor
from ReadWeld.sensors.utils import (
    WeeklyStatistics,
    DailyStatistics,
    NotFindRWSensorException
)


from ReadWeld.api import api


    
class DownloadFileAPI(View):
    
    
    methods = ['POST']
    
    PATH_TO_DB_WITH_FILES = r"C:\Users\Ferre\OneDrive\Документы\Xore4ik\ZIT-ReadWeld\db\sensors"
    
    
    def dispatch_request(self):
        __sensors = Sensor.query.filter_by().all()
        performances = [list(sensor.calculate_performance()) for sensor in __sensors]
        _sensors = [sensor.to_dict() for sensor in __sensors]
        
        year, number_of_week, day = datetime.today().isocalendar()

        return render_template(
            self.template,
            sensors=_sensors,
            performances=performances,
            year=year, number_of_week=number_of_week, day=day,
            masterID=current_user.get_id()
        )
