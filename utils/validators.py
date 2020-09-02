from re import compile

from wtforms.validators import DataRequired, Email

REQUIRED = DataRequired(message="Campo obrigatório.")
VALID_EMAIL = Email(message="Email inválido.")


def _phone_validator(data):
    regex = compile('^\\+258[0-9]{9}$')
    if not regex.match(data['telephone']):
        raise AttributeError('Telefone inválido')

    if not regex.match(data['cellphone']):
        raise AttributeError('Celular inválido')

    if not regex.match(data['fax']):
        raise AttributeError('Fax inválido')


def _nuit_validator(data):
    regex = compile('^[1-9][0-9]{8}$')
    if not regex.match(data['nuit']):
        raise AttributeError('Nuit inválido')


def validate_company(data):
    for validator in [_nuit_validator, _phone_validator]:
        validator(data)
