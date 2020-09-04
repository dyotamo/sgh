from flask_wtf import FlaskForm
from wtforms import IntegerField, DateTimeField, SelectField

from models import Company
from utils.validators import REQUIRED
from utils.extra import get_model_tuple


class ReservationForm(FlaskForm):
    check_in_time = DateTimeField('Check In', validators=[REQUIRED])
    check_out_time = DateTimeField('Check Out', validators=[REQUIRED])
    adult_number = IntegerField('Adultos', validators=[REQUIRED])
    children_number = IntegerField('Crianças', validators=[REQUIRED])
    company = SelectField('Empresa', choices=get_model_tuple(Company))
