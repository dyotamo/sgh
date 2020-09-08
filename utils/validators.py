from re import compile
from typing import Dict
from datetime import datetime

from wtforms.validators import DataRequired, Email


REQUIRED = DataRequired(message="Campo obrigatório.")
EMAIL = Email(message="Email inválido.")


def _valid_phone(data: Dict[str, str]):
    regex = compile('^\\+258[0-9]{9}$')
    if not regex.match(data['telephone']):
        raise AttributeError(
            'Oops, o número do telefone é inválido (deve possuir o formato: +258XXXXXXXXX).')


def _valid_cell(data: Dict[str, str]):
    regex = compile('^\\+258[0-9]{9}$')
    if not regex.match(data['cellphone']):
        raise AttributeError(
            'Oops, o número do celular é inválido (deve possuir o formato: +258XXXXXXXXX).')


def _valid_fax(data: Dict[str, str]):
    regex = compile('^\\+258[0-9]{9}$')
    if not regex.match(data['fax']):
        raise AttributeError(
            'Oops, o número do fax é inválido (deve possuir o formato: +258XXXXXXXXX).')


def _valid_nuit(data):
    regex = compile('^[1-9][0-9]{8}$')
    if not regex.match(data['nuit']):
        raise AttributeError('Oops, o NUIT é inválido.')


def _valid_date(data):
    check_in = data['check_in_time']
    check_out = data['check_out_time']

    if check_in <= datetime.now().date():
        raise AttributeError(
            'Oops, a data do Check-In não pode inferior a data actual.')

    if check_in > check_out:
        raise AttributeError(
            'Oops, a data do Check-In não pode superior a data do Check-Out.')


def validate_company(data: Dict[str, str]):
    for validator in [_valid_phone, _valid_cell, _valid_fax, _valid_nuit]:
        validator(data)


def validate_guest(data: Dict[str, str]):
    for validator in [_valid_cell]:
        validator(data)


def validate_reservation(data: Dict[str, str]):
    for validator in [_valid_date]:
        validator(data)
