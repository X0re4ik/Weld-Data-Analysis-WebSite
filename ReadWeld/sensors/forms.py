from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from ReadWeld.models import Worker, Master, WeldingWireDiameter, WeldMetal, Sensor, WeldingGas


class SensorForm(FlaskForm):
    
    device_name = StringField('Название:',
                           validators=[DataRequired()])
    location = StringField('Расположение:',
                           validators=[])
    
    measurement_period = SelectField('Период измерения',
                            choices=[
                                (1, "1 сек."),
                                (2, "2 сек."),
                                (3, "3 сек.")])
    
    begining_of_work_day = IntegerField("Начало рабочего дня", 
                                        validators=[DataRequired(), NumberRange(min=1, max=12)], 
                                        default=6)
    end_of_working_day = IntegerField("Конец рабочего дня", 
                                      validators=[DataRequired(), NumberRange(min=13, max=23)], 
                                      default=19)
    
    _workers = [(worker.id, f"{worker.first_name} {worker.second_name}/{worker.phone}") for worker in Worker.query.filter_by().all()]
    _workers.insert(0, ('', "Отсуствует"))
    worker_id = SelectField('Отвественный рабочий: ',
                            choices=_workers)
    
    _welding_wire_diameters = [(wwd.id, f"{wwd.diameter} мм.") for wwd in WeldingWireDiameter.query.filter_by().all()]
    welding_wire_diameter_id = SelectField('Диаметр проволки: ',
                            choices=_welding_wire_diameters)
    
    _weld_metals = [(wm.id, f"{wm.density}/{wm.steel_name}") for wm in WeldMetal.query.filter_by().all() ]
    weld_metal_id = SelectField('Металл: ',
                            choices=_weld_metals)
    
    _welding_gases = [ (wg.id, wg.name) for wg in WeldingGas.query.filter_by().all() ]
    welding_gas_id = SelectField('Газ: ',
                            choices=_welding_gases)

    submit = SubmitField('Изменить')
    

    



