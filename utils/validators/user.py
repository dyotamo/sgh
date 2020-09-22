from email_validator import validate_email, EmailNotValidError

from dao import get_where
from models import User


def valid_unique_email(obj):
    ''' o email do usuário deve ser único  '''
    if get_where(User, email=obj.email):
        raise AttributeError('O email informado deve ser único')


def valid_email(obj):
    ''' o email do usuário deve ser válido  '''
    try:
        validate_email(obj.email)
    except EmailNotValidError:
        raise AttributeError('O email informado é inválido')


def validate_user(obj):
    ''' valida o usuário '''
    for validator in [valid_unique_email, valid_email]:
        validator(obj)
