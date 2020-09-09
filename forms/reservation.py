from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, SelectField

from models import Company
from utils.validators import REQUIRED
from utils.extra import get_model_tuple


class ReservationForm(FlaskForm):
    adult_number = IntegerField('Adultos', validators=[REQUIRED])
    children_number = IntegerField('Crianças', validators=[REQUIRED])
    company = SelectField('Em nome de', choices=get_model_tuple(Company))
    check_in_time = DateField('Data do Check In', validators=[
                              REQUIRED], format='%d/%m/%Y')
    check_out_time = DateField('Data do Check Out', validators=[
                               REQUIRED], format='%d/%m/%Y')
