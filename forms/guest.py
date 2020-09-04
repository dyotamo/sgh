from flask_wtf import FlaskForm
from wtforms import TextField, SelectField, IntegerField

from models import Company
from utils.validators import REQUIRED
from utils.constants import ID_TYPES, GENDERS, MARITAL_STATUSES
from utils.extra import get_model_tuple


class GuestForm(FlaskForm):
    name = TextField('Nome', validators=[REQUIRED])
    age = IntegerField('Idade', validators=[REQUIRED])
    id_type = SelectField('Tipo de Documento', validators=[
                          REQUIRED], choices=ID_TYPES)
    id_number = TextField('Número de Documento', validators=[REQUIRED])
    address = TextField('Endereço', validators=[REQUIRED])
    cellphone = TextField('Celular', validators=[REQUIRED])
    father_name = TextField('Nome do Pai')
    mother_name = TextField('Nome da Mãe')
    marital_status = SelectField('Estado Civil', validators=[
        REQUIRED], choices=MARITAL_STATUSES)
    nationality = TextField('Nacionalidade', validators=[REQUIRED])
    company = SelectField('Empresa', choices=get_model_tuple(Company))
    gender = SelectField('Gênero', choices=GENDERS)
