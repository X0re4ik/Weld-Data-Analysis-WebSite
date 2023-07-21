from isoweek import Week
from typing import Tuple
from datetime import datetime, date, timedelta

from ReadWeld.models import (
    Sensor,
    Measurement, Worker, 
    DailyReport)

class LackOfStatisticsForPeriodException(Exception):
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end
        self.message = f"За данный период (c {self.start} по {self.end}) отсутсвует какая-либо статистика"
        super().__init__(self.message)
     
class __Statistics:
    def __init__(self, mac_address: str, start: datetime, end: datetime) -> None:
        self.sensor = Sensor.query.filter_by(mac_address=mac_address).first()
        if not self.sensor:
            raise RuntimeError(
                f"Устройство с MAC-адрессом {mac_address} не найдено"
            )
        self.start  = start
        self.end    = end
        
        self.daily_reports = self.distribution_entries_by_day_of_week()
        if (len(self.daily_reports) == 0) or not (True in [daily_report != None for daily_report in self.daily_reports]):
            raise LackOfStatisticsForPeriodException(self.start, self.end)

    
    def distribution_entries_by_day_of_week(self):
        records = []
        for i in range((self.end - self.start).days + 1):
            date = self.start + timedelta(days=i)
            daily_report = DailyReport.query.filter_by(
                sensor_id=self.sensor.id,
                date=date
                ).first()
            records.append(daily_report)
        return records
        

    def calculation_of_spent_wire_and_gas(self):
        expended_wire = 0
        expended_gas = 0
        for daily_report in self.daily_reports:
            if daily_report: 
                expended_wire += daily_report.expended_wire
                expended_gas += daily_report.expended_gas
        return (expended_wire, expended_gas)

    
    def calculation_work_and_idle_time(self) -> Tuple:
        work_time = 0
        idle_time = 0
        for daily_report in self.daily_reports:
            if daily_report: 
                work_time += daily_report.running_time_in_seconds
                idle_time += daily_report.idle_time_in_seconds
        return (work_time, idle_time)
    
    def get_list_of_daily_reports(self):
        answer = []
        
        for i, daily_report in enumerate(self.daily_reports):
            _in_dict = DailyReport.get_template()
            if daily_report:
                _in_dict = daily_report.to_dict()
            else:
                day = self.start + timedelta(days=i)
                _in_dict['date'] = {
                    "yaer": day.year,
                    "month": day.month,
                    "day": day.day
                }
            answer.append(_in_dict)
        return answer

class WeeklyStatistics(__Statistics):
    
    def __init__(self, mac_address: str, year: int, number_of_week: int) -> None:
        week = Week(year, number_of_week)
        super().__init__(mac_address, week.monday(), week.sunday())
        
    
    def best_report(self):
        return sorted(self.daily_reports, key=lambda daily_report: daily_report.running_time_in_seconds if daily_report else 0)[-1]

    def best_worker(self):
        performance_table  = dict()
        for daily_report in self.daily_reports:
            if daily_report:
                worker_id = daily_report.worker_id
                if worker_id:
                    performance_table[worker_id] = 0
                    performance_table[worker_id] += daily_report.running_time_in_seconds
        
        if not len(performance_table): return None
        best_worker_id = max(performance_table, key=performance_table.get)
        return Worker.query.filter_by(id=best_worker_id).first()

class DailyStatistics(__Statistics):
    
    def __init__(self, mac_address: str, yaer: int, month: int, day: int) -> None:
        __start = date(yaer, month, day)
        __end = __start + timedelta(days=1)
        super().__init__(mac_address, __start, __start)
        
        
    
    
    def __get_measurements_for_period(self, start: datetime, end: datetime):
        return Measurement.query.filter(
            (Measurement.utc_time.between(start,end) &
            (Measurement.sensor_id == self.sensor.id))).all()
        
    
    def _get_measurements_for_period(self, start: datetime, end: datetime):
        
        answer = {
            "amperage": 0,
            "gas_consumption": 0,
            "wire_consumption": 0,
            "performance": 0,
            "date": start.strftime("%Hh %Mm")
        }
        
        measurements = self.__get_measurements_for_period(start, end)        
        for measurement in measurements:
            answer["amperage"]              = (answer["amperage"] + measurement.amperage) / 2
            answer["gas_consumption"]       = (answer["gas_consumption"] + measurement.gas_consumption) / 2
            answer["wire_consumption"]      = (answer["wire_consumption"] + measurement.wire_consumption) / 2
        
        answer["performance"] = (len(measurements) / (end - start).total_seconds()) * 100
        return answer
        
    
    def collect_measurements(self, step_in_minutes=15):
        
        reference_point = datetime(
            year=self.start.year,
            month=self.start.month,
            day=self.start.day,
            hour=self.sensor.begining_of_work_day)
        
        end_of_countdown = datetime(
            year=self.start.year,
            month=self.start.month,
            day=self.start.day,
            hour=self.sensor.end_of_working_day)
        
        
        results = []
        step = timedelta(minutes=step_in_minutes) 
        
        for i in range(int((end_of_countdown.hour - reference_point.hour) * 60 / step_in_minutes)):
            current_time = reference_point + step * i
            results.append(self._get_measurements_for_period(current_time, current_time+step))
            
        return results


