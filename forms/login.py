from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email

REQUIRED = DataRequired(message="Campo obrigatório.")
EMAIL = Email(message="Email inválido.")


class LoginForm(FlaskForm):
    email = TextField('Email', validators=[REQUIRED, EMAIL])
    password = PasswordField('Senha', validators=[REQUIRED])
