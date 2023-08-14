
from typing import Any
from ReadWeld.models import Sensor

from functools import wraps


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