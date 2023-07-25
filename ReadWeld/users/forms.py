from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError

from wtforms.widgets import PasswordInput

from flask_login import current_user
from ReadWeld.models import Worker, Master


from flask import request


class SubmitEdit(FlaskForm):
    submit = SubmitField('Изменить')
    
    
class SubmitAdd(FlaskForm):
    submit = SubmitField('Добавить')
    
    





class WorkerForm(FlaskForm):
    first_name = StringField('Имя:',
                           validators=[DataRequired()])
    second_name = StringField('Фамилия:',
                              validators=[DataRequired()])
    phone = StringField('Телефон:', validators=[DataRequired(), Length(10, 12)])
    


class MasterForm(WorkerForm):
    email = StringField('Email:',
                        validators=[DataRequired(), Email()])
    
    notification = BooleanField('Получать уведомления?')
    
class WelderForm(WorkerForm):
    category = SelectField('Квалификация',
                           choices=[
                                ("A2", "A2 (2 и 3 разряд)"), 
                                ("B3", "B3 (4 и 5 разряд)"), 
                                ("C4", "C4 (6 разряд)"), 
                                ("D4", "D4 (бригадир)")],
                           validators=[DataRequired()]) 



class ChecksForWelder(FlaskForm):
    def validate_phone(self, phone):
        user = Worker.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError(
                'Этот телефон занят. Пожалуйста, выберите другой.')


class ChecksForMasters(ChecksForWelder):
    def validate_email(self, email):
        user = Master.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Этот email занят. Пожалуйста, выберите другой.')
            
class MasterRegistration(MasterForm, ChecksForMasters, SubmitAdd):
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердить пароль',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])

class MasterLoginForm(FlaskForm):
    phone = StringField('Телефон:', validators=[DataRequired(), Length(10, 12)])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    
    submit = SubmitField('Войти')


class WelderRegistration(WelderForm, SubmitAdd, ChecksForWelder):
    pass


class WorkerUpdate(WorkerForm):
    
    def __validate_changed_password(self, old_phone):
        new_phone = self.phone.data
        if old_phone != new_phone:
            user = Worker.query.filter_by(phone=new_phone).first()
            if user:
                raise ValidationError(
                    'Этот телефон занят. Пожалуйста, выберите другой.')
                    
    def _validate_changed_password(self, old_phone) -> bool:
        is_valid = True
        try:
            self.__validate_changed_password(old_phone)
        except ValidationError as e:
            self.phone.errors = (str(e),)
            is_valid = False
        return is_valid
                    
    def validate_on_submit(self, *args, **kwargs):
        result = super().validate_on_submit()
        
        old_phone = kwargs["old_phone"]

        return result and self._validate_changed_password(old_phone)
    
    

class MasterUpdate(WorkerUpdate, MasterForm, SubmitEdit):
    
    def __validate_changed_email(self, old_email):
        new_email = self.email.data
        if new_email != old_email:
            user = Master.query.filter_by(email=new_email).first()
            if user:
                raise ValidationError(
                    'Этот email занят. Пожалуйста, выберите другой.')
    
    def _validate_changed_email(self, old_email) -> bool:
        is_valid = True
        try:
            self.__validate_changed_email(old_email)
        except ValidationError as e:
            self.email.errors = (str(e),)
            is_valid = False
        return is_valid
    
    def validate_on_submit(self, *args, **kwargs):

        old_phone = kwargs["old_phone"]
        result = WorkerUpdate().validate_on_submit(old_phone = old_phone)
        old_email = kwargs["old_email"]
        return result and self._validate_changed_email(old_email)

class WelderUpdate(WorkerUpdate, WelderForm, SubmitEdit):
    pass

