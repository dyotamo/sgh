from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField

from utils.validators import REQUIRED


class LoginForm(FlaskForm):
    email = TextField('Email', validators=[REQUIRED])
    password = PasswordField('Senha', validators=[REQUIRED])
