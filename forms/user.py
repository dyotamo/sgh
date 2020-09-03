from flask_wtf import FlaskForm
from wtforms import TextField, SelectField

from utils.validators import REQUIRED, EMAIL
from utils.constants import PROFILES


class UserForm(FlaskForm):
    name = TextField('Nome', validators=[REQUIRED])
    email = TextField('Email', validators=[REQUIRED, EMAIL])
    profile = SelectField('Perfil', validators=[REQUIRED], choices=PROFILES)
