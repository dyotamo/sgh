from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, FloatField

from models import RoomType
from utils.validators import REQUIRED
from utils.extra import get_model_tuple


class RoomForm(FlaskForm):
    number = IntegerField('Número', validators=[REQUIRED])
    category = SelectField('Tipo', choices=get_model_tuple(RoomType))
    status = SelectField('Status',
                         validators=[REQUIRED],
                         choices=[('available', 'Disponível'),
                                  ('busy', 'Ocupado'),
                                  ('sweeping', 'Em arrumação'),
                                  ('closed', 'Encerrado')])
    daily_amount = FloatField(validators=[REQUIRED])
