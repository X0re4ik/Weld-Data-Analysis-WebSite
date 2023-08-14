from datetime import datetime
from abc import ABC
from pathlib import Path

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
from ReadWeld.utils import r_if_sensor_not_exist


    
class ShowSensorsView(View):
    """
        Класс отображение всех ReadWeld-датчиков
            methods: 'GET'
    """
    
    methods=['GET']
    decorators = [login_required]
    
    def __init__(self) -> None:
        super().__init__()
        self.template = "/".join(
            ("sensors", "show", "show.html")
        )
    
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
        



class SelectIntervalForDisplayingStatisticsView(View):
    
    methods=["GET"]
    
    decorators = [login_required]
    
    
    def __init__(self) -> None:
        self.template = "/".join(
            ("sensors", "choose", "choose.html")
        )

    def dispatch_request(self):
        sensors = Sensor.query.filter().all()
        sensors = [sensor.to_dict() for sensor in sensors]
        return render_template(
            self.template,
            sensors=sensors,
            masterID=current_user.get_id()
        )
        



class SensorEditView(View):
    
    methods=['POST', "GET"]
    
    decorators = [r_if_sensor_not_exist, login_required]
    
    def __init__(self) -> None:
        self.template = "/".join(
            ("sensors", "edit", "edit.html")
        )
        
    def dispatch_request(self, mac_address: str):
        sensor = Sensor.query.filter_by(mac_address=mac_address).first()
        if not sensor: raise NotFindRWSensorException(mac_address)
        
        form = SensorForm(
            device_name=sensor.device_name,
            location=sensor.location,
            measurement_period=sensor.measurement_period,
            
            worker_id=sensor.worker_id,
            welding_wire_diameter_id=sensor.welding_wire_diameter_id,
            weld_metal_id=sensor.weld_metal_id,
            welding_gas_id=sensor.welding_gas_id,
            
            begining_of_work_day=sensor.begining_of_work_day,
            end_of_working_day=sensor.end_of_working_day
        )
        
        if form.validate_on_submit():
            form.worker_id.data = None if not form.worker_id.data else form.worker_id.data
            form.populate_obj(sensor)
            db.session.commit()
            return redirect(url_for('sensors.edit_settings', mac_address=mac_address))
        
        performances = [list(sensor.calculate_performance())]
        
        return render_template(
            self.template, 
            form=form,
            sensor=sensor.to_dict(),
            performances=performances,
            masterID=current_user.get_id())
    



class _StatisticsView(View, ABC):
    
    methods = ["GET"]
    
    decorators = [login_required]
    
    def __init__(self, _type) -> None:
        title = "weekly" if _type == "w" else "daily"
        title += '.html'
        self.template = "/".join(
            ("sensors", "statistics", title)
        )
        
        self._statistics = None
    
    def __later_init__(self, mac_address: str):
        self._sensor = Sensor.query.filter_by(mac_address=mac_address).first()
        if not self._sensor: raise NotFindRWSensorException(mac_address)
        

    def data_to_dict(self):
        if not self._statistics:
            raise RuntimeError("Объект статистики не определен для класа")
        
        total_work_and_idle_time = list(self._statistics.calculation_work_and_idle_time())
        total_spent_wire_and_gas = list(self._statistics.calculation_of_spent_wire_and_gas())
        performances = [list(self._statistics.calculation_work_and_idle_time())]
        daily_reports = self._statistics.get_list_of_daily_reports()
        
        return {
            "sensor": self._sensor.to_dict(),
            "total_work_and_idle_time": total_work_and_idle_time,
            "total_spent_wire_and_gas": total_spent_wire_and_gas,
            "performances": performances,
            "daily_reports": daily_reports
        }
        
    def dispatch_request(self, mac_address: str):
        self.__later_init__(mac_address)
        
        statistics = self.data_to_dict()
        return render_template(self.template, statistics=statistics, masterID=current_user.get_id())


class WeeklyStatisticsView(_StatisticsView):
    """
        Класс отображение недельной статистики данных за период
            methods: 'GET'
            
            arguments:
                year (int) - год получения статистики\n
                number_of_week (int) - номер недели получения статистики      
    """
    
    def __init__(self) -> None:
        super().__init__('w')

    
    def __later_init__(self, mac_address):
        super().__later_init__(mac_address)
        
        self.year            = int(request.args.get("year"))
        self.number_of_week  = int(request.args.get("number_of_week"))
        
        self._statistics = WeeklyStatistics(
            mac_address, self.year, self.number_of_week
        )
    
    def data_to_dict(self):
        general_data = super().data_to_dict()
        
        best_daily_report               = self._statistics.best_report().to_dict()
        best_worker                     = self._statistics.best_worker()
        best_worker                     = best_worker.to_dict() if best_worker else None
        
        return {
            **general_data,
            "best_daily_report": best_daily_report,
            "best_worker": best_worker
        }      

class DailyStatisticsView(_StatisticsView):
    """
        Класс отображение статистики за конкретный день
            methods: 'GET'
            
            arguments:
                year (int) - год получения статистики\n
                month (int) - месяц получения статистики\n
                day (int) - день получения статистики\n
                interval (int) - период в минутах получения статистики
    """
    
    def __init__(self) -> None:
        super().__init__("d")
    
    
    def __later_init__(self, mac_address):
        super().__later_init__(mac_address)
        
        self.year            = int(request.args.get("year"))
        self.month           = int(request.args.get("month"))
        self.day             = int(request.args.get("day"))
        self.interval        = int(request.args.get("interval") or 15)
        
        self._statistics = DailyStatistics(mac_address, self.year, self.month, self.day)
    
    def data_to_dict(self):
        general_data = super().data_to_dict()
        
        measurements = self._statistics.collect_measurements(self.interval)
        return {
            **general_data,
            "interval": self.interval,
            "measurements": {
                "data": measurements,
                "length": len(measurements)
            }
        }





class ShowFilesView(View):
    
    methods = ["GET"]
    
    decorators = [r_if_sensor_not_exist, login_required]

    PATH_TO_DB_WITH_FILES = r"C:\Users\Ferre\OneDrive\Документы\Xore4ik\ZIT-ReadWeld\db\sensors"
    
    SUPPORTED_FORMATS = ['xlsx']
    
    def __init__(self) -> None:
        super().__init__()
        
        self._template = "/".join(
            ("sensors", "statistics", "files.html")
        )
    
    
    def dispatch_request(self, mac_address: str):
        
        PATH_TO_DIR = Path(self.__class__.PATH_TO_DB_WITH_FILES).joinpath(mac_address)
        
        files = []
        
        if PATH_TO_DIR.exists():
            for PATH_TO_FILE in PATH_TO_DIR.iterdir():
                SUFFIX = PATH_TO_FILE.suffix[1:]
                if SUFFIX in self.__class__.SUPPORTED_FORMATS:
                    DATE_STR = PATH_TO_FILE.name.split('.')[0]
                    files.append(
                        {
                            "date": DATE_STR,
                            SUFFIX: PATH_TO_FILE.name
                        }
                    )
        
        return render_template(
            self._template,
            mac_address=mac_address,
            files=files,
            masterID=current_user.get_id())