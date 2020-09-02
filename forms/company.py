from flask_wtf import FlaskForm
from wtforms import TextField

from utils.validators import REQUIRED, VALID_EMAIL


class CompanyForm(FlaskForm):
    name = TextField('Nome', validators=[REQUIRED])
    nuit = TextField('NUIT', validators=[REQUIRED])
    activity_branch = TextField('Ramo de actividade', validators=[REQUIRED])
    address = TextField('Endereço', validators=[REQUIRED])
    telephone = TextField('Telefone', validators=[REQUIRED])
    fax = TextField('Fax', validators=[REQUIRED])
    cellphone = TextField('Celular', validators=[REQUIRED])
    email = TextField('Email', validators=[REQUIRED, VALID_EMAIL])
