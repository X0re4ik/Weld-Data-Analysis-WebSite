
from typing import Any
from ReadWeld.models import Sensor, DailyReport, Welder

from functools import wraps

from flask import redirect, abort, Response

import json


from datetime import datetime, timedelta

from ReadWeld.models import Master, Worker
from flask import url_for
        

 
def if_sensor_not_exist_404(func) -> Any:
    @wraps(func)
    def wrapper(*args, **kwargs):
        mac_address = kwargs["mac_address"]
        if not Sensor.query.filter(Sensor.mac_address==mac_address).first():
            return abort(404, f'Устройство с таким MAC-адрессом {mac_address} не найдено')
        return func(*args, **kwargs)
    return wrapper

def if_welder_not_exist_404(func) -> Any:
    @wraps(func)
    def wrapper(*args, **kwargs):
        welder_id = kwargs["id"]
        if not Welder.query.filter(Welder.id==welder_id).first():
            return abort(404, f'Сварщик не был найден')
        return func(*args, **kwargs)
    return wrapper



from typing import Optional
from pathlib import Path

from ReadWeld import READ_WELD_WORKDIR



class WorkingWithFileDatabase:
    
    NAME: Optional[str] = None
    FILE_DATABASE: Optional[Path] = None
    DIRS = ["sensors", "users"]
    
    def __init__(self) -> None:
        if self.__class__.NAME is None:
            raise ValueError("NAME не определен")

        self.__class__.FILE_DATABASE = Path.joinpath(READ_WELD_WORKDIR.parent.absolute(), self.__class__.NAME)
        for dir in self.__class__.DIRS:
            path_to = Path.joinpath(self.__class__.FILE_DATABASE, dir)
            path_to.mkdir(exist_ok=True)
            setattr(self, f"PATH_TO_FILES_WITH_{dir.upper()}", path_to)
        
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WorkingWithFileDatabase, cls).__new__(cls)
        return cls.instance


from ReadWeld.models import (
    WeldingWireDiameter, WeldMetal, WeldingGas, 
    Worker, Master)

from ReadWeld.models import db
from typing import List, Tuple, Mapping, Optional

class FillDBWithStandardValues:
    
    STANDARD_WELDING_WIRE_DIAMETERS: List[float] = [0.8, 1.0, 1.2, 1.4, 1.6, 2.0]
    WELDING_WIRES_METAL_AND_IT_DENSITIES: List[Tuple] = [
        ("Сталь", 7700), 
        ("Медь", 8.93*10**3)
    ]
    WELDING_GASES: List[str] = ["Аргон", "Углекислота"]
    
    SCHEME_TABLE_VALUES: Optional[Mapping[db.Model, List]] = None
    
    def __init__(self):
        if self.__class__.SCHEME_TABLE_VALUES is None:
            raise RuntimeError("Схема создания не определена")
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FillDBWithStandardValues, cls).__new__(cls)
        return cls.instance
        
    def fill_table__WeldingWireDiameter(self):
        for standard_welding_wire_diameter in self.__class__.STANDARD_WELDING_WIRE_DIAMETERS:
            welding_wire_diameter = WeldingWireDiameter(diameter=standard_welding_wire_diameter)
            self.add_and_commit_in_db(welding_wire_diameter)

    
    def fill_table__WeldMetal(self):
        for steel_name, density in self.__class__.WELDING_WIRES_METAL_AND_IT_DENSITIES:
            weld_metal = WeldMetal(steel_name=steel_name, density=density)
            self.add_and_commit_in_db(weld_metal)


    def fill_table__WeldingGas(self):
        for welding_gas in self.__class__.WELDING_GASES:
            self.add_and_commit_in_db(WeldingGas(name=welding_gas))


    def fill_table__Master(self):
        worker_id = self.add_and_commit_in_db(Worker(first_name="Anton", second_name="Mochalov", phone="+79923458625"))
        master_id = self.add_and_commit_in_db(Master(email="ZIT@yandex.ru", password="ZIT", notification=False, worker_id=worker_id))
            
    def __fill(self):
        for table, method_ in self.__class__.SCHEME_TABLE_VALUES.items():
            if not table.query.filter_by().first():
                method_(self)
    
    @staticmethod
    def fill():
        FillDBWithStandardValues().__fill()
    
        
    @staticmethod
    def add_and_commit_in_db(row) -> int:
        db.session.add(row)
        db.session.commit()
        return row.id


FillDBWithStandardValues.SCHEME_TABLE_VALUES: Mapping[db.Model, List] = {
        WeldingWireDiameter: FillDBWithStandardValues.fill_table__WeldingWireDiameter,
        WeldMetal: FillDBWithStandardValues.fill_table__WeldMetal,
        WeldingGas: FillDBWithStandardValues.fill_table__WeldingGas,
        Master: FillDBWithStandardValues.fill_table__Master
}


class JinjaHelper:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(JinjaHelper, cls).__new__(cls)
        return cls.instance
    
    
    @staticmethod
    def python_object_to_json(__object):
        return json.dumps(__object)
    
    @staticmethod
    def init_app(app):
        app.jinja_env.globals.update(
            python_object_to_json=JinjaHelper.python_object_to_json)
        app.jinja_env.globals.update(working_hours=JinjaHelper.working_hours)
        app.jinja_env.globals.update(date_on_day_of_week=JinjaHelper.date_on_day_of_week)
        app.jinja_env.globals.update(worker=JinjaHelper.worker)
        app.jinja_env.globals.update(sensor_info=JinjaHelper.sensor_info)
        
        app.jinja_env.globals.update(about_sensor=JinjaHelper.about_sensor)
        app.jinja_env.globals.update(about_worker=JinjaHelper.about_worker)
        app.jinja_env.globals.update(about_master=JinjaHelper.about_master)

    @staticmethod
    def load(app):
        app.jinja_env.globals.update(
            python_object_to_json=JinjaHelper.python_object_to_json)
        app.jinja_env.globals.update(working_hours=JinjaHelper.working_hours)
        app.jinja_env.globals.update(date_on_day_of_week=JinjaHelper.date_on_day_of_week)
        app.jinja_env.globals.update(worker=JinjaHelper.worker)
        app.jinja_env.globals.update(sensor_info=JinjaHelper.sensor_info)
        
        app.jinja_env.globals.update(about_sensor=JinjaHelper.about_sensor)
        app.jinja_env.globals.update(about_worker=JinjaHelper.about_worker)
        app.jinja_env.globals.update(about_master=JinjaHelper.about_master)
        
        
        
    
    
    @staticmethod
    def date_on_day_of_week(year, month, day, language='ru') -> str:
        day_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        date = datetime(year=year, month=month, day=day)
        return day_of_week[date.weekday()]
    
    @staticmethod
    def working_hours(seconds: int):
        hour = seconds // 3600
        seconds %= 3600 
        minutes = seconds // 60 
        seconds %= 60
        return f"{hour} ч {minutes} мин {seconds} с"
    
    @staticmethod
    def worker(worker_in_dict: dict):
        print(worker_in_dict)
        value = worker_in_dict["first_name"] + " " + worker_in_dict["second_name"]
        value = "{0} {1} ({2})".format(
            worker_in_dict["first_name"],
            worker_in_dict["second_name"],
            worker_in_dict["phone"]
        )
        href = "url_for('weekly-statistics-view', id={})".format(worker_in_dict["id"])
        return [value, href]

    
    @staticmethod
    def about_worker(worker: dict):
        keys = ["title", "href"]
        is_valid = worker and len(worker) != 0
        if not is_valid: return None
        values = [
            worker["first_name"] + " " + worker["second_name"],
            f"/users/welder/{worker['id']}/edit"
        ]
        
        return dict(zip(keys, values))

    @staticmethod
    def sensor_info(sensor: dict):
        return "MAC: {0}\nНазвание: {1}\nРасположение: {2}\nСварщик {3}".format(
            sensor["mac_address"],
            sensor["device_name"],
            sensor["location"],
            JinjaHelper.worker(sensor["worker"])[0]
        )
        
    @staticmethod
    def about_sensor(sensor: dict):
        keys = ["mac", "name", "worker", "href", "cheats"]
        is_valid = sensor and len(sensor) != 0
        if not is_valid: return None
        
        mac = sensor["mac_address"]
        name = sensor["device_name"]
        worker = JinjaHelper.about_worker(sensor["worker"])
        href = url_for("sensors.edit_settings", mac_address=mac)
        cheats = "MAC: {0}\nНазвание: {1}\nРасположение: {2}\nСварщик: {3}".format(
            mac,
            name,
            sensor["location"],
            worker["title"] if worker else None  
        )

        values = [
            mac, name, worker, href, cheats
        ]
        return dict(zip(keys, values))
    
    def about_master(worker_id):
        master = Master.query.filter(Master.worker_id == worker_id).first()
        if not master: return None
        worker = Worker.query.filter(Worker.id == worker_id).first()
        href = url_for("users.edit_master", id=worker.id)
        keys = ["title", "href"]
        values = [
            worker.first_name + " " + worker.second_name, href
        ]
        return dict(zip(keys, values))
        
        
jinja_helper = JinjaHelper()       