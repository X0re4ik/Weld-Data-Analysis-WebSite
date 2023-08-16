
from typing import Any
from ReadWeld.models import Sensor

from functools import wraps

class envNotFound(Exception):
    def __init__(self, path) -> None:
        self._message = f"""
    Cруктура проекта должна быть следующая:
        |-<папка web сервиса>
            |-ReadWeld
            |-.env
            |-run.py
    
    В данном приложении отсутсвует .env файл.
    env файл содержит основные настройки web-приложения
    Обязательные аргументы, входящте в env файл:
    
        #Секретный ключ Flask
        FLASK_SECRET_KEY            = "..."

        # Настройки приложения
        APP_HOST                    = "..."
        APP_PORT                    = "..."
        APP_DEBUG                   = "..."

        # Настройки базы данных
        DATA_BASE_USERNAME          = "..."
        DATA_BASE_PASSWORD          = ".."
        DATA_BASE_HOST              = "..."
        DATA_BASE_PORT              = "..."
        DATA_BASE_NAME              = "..."

        #Прочие настройки
        PATH_TO_DB_WITH_FILES       = "..."

    При запуске приложение искало env в директории:
        {path}
"""
        super().__init__(self._message)
        


class SensorNotFoundException(Exception):
    def __init__(self, mac_address) -> None:
        self._message = f"Устройство с MAC адрессом - {mac_address} не найдено."
    
def r_if_sensor_not_exist(func) -> Any:
    @wraps(func)
    def wrapper(*args, **kwargs):
        mac_address = kwargs["mac_address"]
        if not Sensor.query.filter(Sensor.mac_address==mac_address).first():
            raise RuntimeError("!"*100)
        return func(*args, **kwargs)
    return wrapper