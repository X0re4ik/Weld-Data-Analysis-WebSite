
import json


from datetime import datetime, timedelta 
class JinjaHelper:
    
    
    @staticmethod
    def python_object_to_json(__object):
        return json.dumps(__object)

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
        href = f"/sensor/{mac}/edit"
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
        
        
        