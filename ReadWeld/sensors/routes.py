from ReadWeld.sensors import sensors

from ReadWeld.sensors.controllers import (
    DailyStatisticsView,
    WeeklyStatisticsView,
    ShowSensorsView,
    SelectIntervalForDisplayingStatisticsView,
    SensorEditView,
    ShowFilesView
)

sensors.add_url_rule("/sensors/show", 
                     view_func=ShowSensorsView.as_view("show-sensors"))

sensors.add_url_rule("/sensors/<string:mac_address>/edit", 
                     view_func=SensorEditView.as_view("edit_settings"))

sensors.add_url_rule("/sensors/statistics", 
                     view_func=SelectIntervalForDisplayingStatisticsView.as_view("statistics"))

sensors.add_url_rule("/sensors/statistics/<string:mac_address>/daily", 
                     view_func=DailyStatisticsView.as_view("daily-statistics-view"))

sensors.add_url_rule("/sensors/statistics/<string:mac_address>/weekly", 
                     view_func=WeeklyStatisticsView.as_view("weekly-statistics-view"))


sensors.add_url_rule("/sensors/statistics/<string:mac_address>/files",
                     view_func=ShowFilesView.as_view("show-files-view"))