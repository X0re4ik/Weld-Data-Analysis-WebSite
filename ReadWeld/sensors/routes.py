from ReadWeld.sensors import sensors

from ReadWeld.sensors.controllers import (
    DailyStatisticsView,
    WeeklyStatisticsView,
    ShowSensorsView
)


sensors.add_url_rule("/sensor/show", 
                     view_func=ShowSensorsView.as_view("show-sensors"))

sensors.add_url_rule("/sensor/<string:mac_address>/statistics/daily", 
                     view_func=DailyStatisticsView.as_view("daily-statistics-view"))

sensors.add_url_rule("/sensor/<string:mac_address>/statistics/weekly", 
                     view_func=WeeklyStatisticsView.as_view("weekly-statistics-view"))