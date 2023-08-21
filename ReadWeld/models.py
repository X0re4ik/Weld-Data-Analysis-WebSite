from sqlalchemy import UniqueConstraint
from typing import List, Tuple, Dict


from datetime import datetime
from ReadWeld import db



class ModelAsDict:
    
    def as_dict(self, deep=True):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Sensor(db.Model, ModelAsDict):
    __tablename__ = "sensor"
    
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(30), unique=True, nullable=False)
        
    device_name = db.Column(db.String(30), nullable=False, default="ReadWeld#...")
    location = db.Column(db.String(150), nullable=True)
    measurement_period = db.Column(db.Integer, default=1)
    
    begining_of_work_day = db.Column(db.Integer, nullable=False, default=6)
    end_of_working_day = db.Column(db.Integer, nullable=False, default=18)
    
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=True)
    welding_wire_diameter_id = db.Column(db.Integer, db.ForeignKey('welding_wire_diameter.id'), nullable=False, default=1)
    weld_metal_id = db.Column(db.Integer, db.ForeignKey('weld_metal.id'), nullable=False, default=1)
    welding_gas_id = db.Column(db.Integer, db.ForeignKey('welding_gas.id'), nullable=False, default=1)
    
    daily_reports = db.relationship('DailyReport', backref='Sensor', lazy='dynamic')

    
    def get_worker(self):
        if not self.worker_id: return None
        return Worker.query.filter_by(id=self.worker_id).first()
    
    def get_welding_wire_diameter(self):
        return WeldingWireDiameter.query.filter_by(id=self.welding_wire_diameter_id).first()
    
    def get_weld_metal(self):
        return WeldMetal.query.filter_by(id=self.weld_metal_id).first()

    def calculate_performance(self) -> Tuple:
        running_time_in_seconds = 0
        idle_time_in_seconds = 0
        for daily_report in DailyReport.query.filter_by(sensor_id=self.id).all():
            running_time_in_seconds     += daily_report.running_time_in_seconds
            idle_time_in_seconds        += daily_report.idle_time_in_seconds
        return (running_time_in_seconds, idle_time_in_seconds)
    
    def to_dict(self, deep=True):
        answer = {
            "id": self.id,
            "mac_address": self.mac_address,
            "device_name": self.device_name,
            "location": self.location,
            "measurement_period": self.measurement_period,
            "worker": self.get_worker(),
            "welding_wire_diameter": self.get_welding_wire_diameter(),
            "weld_metal": self.get_weld_metal(),
        }
        if deep:
            value_or_null = lambda value: value.to_dict() if value else None
            answer["worker"] = value_or_null(answer["worker"])
            answer["welding_wire_diameter"] = value_or_null(answer["welding_wire_diameter"])
            answer["weld_metal"] = value_or_null(answer["weld_metal"])
        return answer

    def __repr__(self):
        return f'<Setting {self.id}>'



class Worker(db.Model):
    __tablename__ = "worker"
    
    id = db.Column(db.Integer, primary_key=True)
    
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(12), nullable=False, unique=True)
    
    daily_reports = db.relationship('DailyReport', backref='Worker', lazy='dynamic')
    
    def calculate_performance(self) -> Tuple:
        running_time_in_seconds = 0
        idle_time_in_seconds = 0
        for daily_report in DailyReport.query.filter_by(worker_id=self.id).all():
            running_time_in_seconds     += daily_report.running_time_in_seconds
            idle_time_in_seconds        += daily_report.idle_time_in_seconds
        return (running_time_in_seconds, idle_time_in_seconds)
    
    def __repr__(self):
        return f'<Worker {self.first_name}-{self.second_name}>'
    
    
    def to_dict(self, deep: bool = True):
        answer = {
            "id": self.id,
            "first_name": self.first_name,
            "second_name": self.second_name,
            "phone": self.phone,
        } 
        return answer
        

    
    
class Master(db.Model):
    __tablename__ = "master"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    notification = db.Column(db.Boolean, default=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))
    
    @staticmethod
    def exist(phone):
        worker = Worker.query.filter(Worker.phone == phone).first()
        if worker:
            master = Master.query.filter(Master.worker_id == worker.id).first()
            return master
        return None
        

    
class Welder(db.Model):
    __tablename__ = "welder"
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(2), nullable=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))
    
    
    def to_dict(self, deep=True) -> Dict:
        worker = Worker.query.filter_by(id=self.worker_id).first()
        return {
            "id": self.id, 
            "worker": worker,
            "first_name": worker.first_name,
            "second_name": worker.second_name,
            "phone": worker.phone,
            "category": self.category
        }
    

    
    
class WeldingWireDiameter(db.Model):
    __tablename__ = "welding_wire_diameter"
    
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.Float, unique=True, nullable=False)
    
    def to_dict(self, deep=True):
        answer = {
            "id": self.id,
            "diameter": self.diameter
        }
        return answer
    
    @staticmethod
    def get_id_of_wire_diameter(diameter: float):
        return WeldingWireDiameter.query.filter_by(diameter=diameter).first()
    
    @staticmethod
    def get_all_row(self):
        return WeldingWireDiameter.query.filter_by().all()
        
        
    
class WeldMetal(db.Model):
    __tablename__ = "weld_metal"
    
    id = db.Column(db.Integer, primary_key=True)
    steel_name = db.Column(db.String(50), unique=True, nullable=False)
    density = db.Column(db.Float, nullable=False)
    
    def to_dict(self, deep=True):
        return {
            "id": self.id,
            "steel_name": self.steel_name,
            "density": self.density,
        }
    
    @staticmethod
    def get_id_of_metal(steel_name: str):
        return WeldMetal.query.filter_by(steel_name=steel_name).first()



class Measurement(db.Model):
    __tablename__ = "measurement"
    
    id = db.Column(db.Integer, primary_key=True)
    
    utc_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    amperage = db.Column(db.Integer, nullable=False)
    gas_consumption = db.Column(db.Integer, nullable=False) # л/мин
    wire_consumption = db.Column(db.Integer, nullable=False) # кг/час
    
    
    def __repr__(self):
        return f'<Measurement {self.utc_time}:{self.amperage};{self.gas_consumption};{self.wire_consumption}.>'

    def to_dict(self, deep=True):
        return {
            "id": self.id,
            "utc_time": self.utc_time, 
            "amperage": self.amperage,
            "gas_consumption": self.gas_consumption,
            "wire_consumption": self.wire_consumption
        }
    



class DailyReport(db.Model):
    __tablename__ = "daily_report"
    
    id = db.Column(db.Integer, primary_key=True)
    
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)    
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    __table_args__ = (UniqueConstraint('sensor_id', 'date', name='_sensor_date_'), )
    
    # Средние значения
    average_amperage = db.Column(db.Float, nullable=False)
    average_gas_consumption = db.Column(db.Float, nullable=False)
    average_wire_consumption = db.Column(db.Float, nullable=False)
    
    # Израсходовано
    expended_wire = db.Column(db.Float, nullable=False)
    expended_gas = db.Column(db.Float, nullable=False)
    
    # Максимальные значения
    max_amperage = db.Column(db.Float, nullable=False)
    max_gas_consumption = db.Column(db.Float, nullable=False)
    max_wire_consumption = db.Column(db.Float, nullable=False)
    
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=True)
    welding_wire_diameter_id = db.Column(db.Integer, db.ForeignKey('welding_wire_diameter.id'), nullable=False)
    weld_metal_id = db.Column(db.Integer, db.ForeignKey('weld_metal.id'), nullable=False)
    welding_gas_id = db.Column(db.Integer, db.ForeignKey('welding_gas.id'), nullable=False)
    
    
    # Время работы, простоя
    running_time_in_seconds = db.Column(db.Integer, nullable=False)
    idle_time_in_seconds = db.Column(db.Integer, nullable=False)
    
    
    
    def get_Sensor(self):
        return Sensor.query.filter_by(id=self.sensor_id).first()
    
    def get_Worker(self):
        return Worker.query.filter_by(id=self.worker_id).first() if self.worker_id else None
    
    def get_WeldingWireDiameter(self):
        return WeldingWireDiameter.query.filter_by(
                id=self.welding_wire_diameter_id).first()
    
    def get_WeldMetal(self):
        return WeldMetal.query.filter_by(id=self.weld_metal_id).first()
    
    def get_WeldingGas(self):
        return WeldingGas.query.filter_by(id=self.welding_gas_id).first()
    
    @staticmethod
    def get_template():
        return {
            'id': 0,            
            'date': None,
            
            'average_amperage': 0,
            'average_gas_consumption': 0,
            "average_wire_consumption": 0,
            
            'expended_wire': 0,
            'expended_gas': 0,
            
            'max_amperage': 0,
            'max_gas_consumption': 0,
            "max_wire_consumption": 0,
            
            'sensor': None,
            'worker': None,
            'welding_wire_diameter': None,
            "weld_metal": None,
            
            'running_time_in_seconds': 0,
            'idle_time_in_seconds': 0
        }
    
    def to_dict(self, deep=True) -> Dict:
        answer = {
            'id': self.id,            
            'date': self.date,
            
            'average_amperage': self.average_amperage,
            'average_gas_consumption': self.average_gas_consumption,
            "average_wire_consumption": self.average_wire_consumption,
            
            'expended_wire': self.expended_wire,
            'expended_gas': self.expended_gas,
            
            'max_amperage': self.max_amperage,
            'max_gas_consumption': self.max_gas_consumption,
            "max_wire_consumption": self.max_wire_consumption,
            
            'sensor': self.get_Sensor(),
            'worker': self.get_Worker(),
            'welding_wire_diameter': self.get_WeldingWireDiameter(),
            "weld_metal": self.get_WeldMetal(),
            "welding_gas": self.get_WeldingGas(),
            
            'running_time_in_seconds': self.running_time_in_seconds,
            'idle_time_in_seconds': self.idle_time_in_seconds
        }
        
        if deep:
            value_or_null = lambda value: value.to_dict() if value else None
            answer["worker"] = value_or_null(answer["worker"])
            answer["welding_wire_diameter"] = value_or_null(answer["welding_wire_diameter"])
            answer["sensor"] = value_or_null(answer["sensor"])
            answer["weld_metal"] = value_or_null(answer["weld_metal"])
            answer["welding_gas"] = value_or_null(answer["welding_gas"])
            
            answer["date"] = {
                "year": self.date.year,
                "month": self.date.month,
                "day": self.date.day
            }
            
        return answer


class WeldingGas(db.Model):
    __tablename__ = "welding_gas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    def to_dict(self, deep=True):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}