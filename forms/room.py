from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, FloatField

from utils.validators import REQUIRED


class RoomForm(FlaskForm):
    number = IntegerField('Número', validators=[REQUIRED])
    category = SelectField('Categoria',
                           validators=[REQUIRED],
                           choices=[('single', 'Solteiro'),
                                    ('couple', 'Casal')])
    status = SelectField('Status',
                         validators=[REQUIRED],
                         choices=[('available', 'Disponível'),
                                  ('busy',
                                   'Ocupado'),
                                  ('sweeping',
                                   'Em arrumação'),
                                  ('closed', 'Encerrado')])
    daily_amount = FloatField(validators=[REQUIRED])
