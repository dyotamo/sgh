from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, SelectField

from models import Room, Guest
from utils.validators import REQUIRED
from utils.extra import get_model_tuple


class CheckInForm(FlaskForm):
    room = SelectField('Quarto', choices=get_model_tuple(Room, 'number'))
    check_out_time = DateField('Data do Check Out', validators=[
                               REQUIRED], format='%d/%m/%Y')


class CheckInGuestForm(FlaskForm):
    guest = SelectField('Hóspede', choices=get_model_tuple(Guest))
