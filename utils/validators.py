from re import compile
from typing import Dict
from datetime import datetime

from wtforms.validators import DataRequired, Email

from dao import get
from models import Room


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
    current_date = datetime.now().date()

    # Se a data do check in não for informada,
    # significa que estamos a considerar a data corrente
    check_in = data.get('check_in_time') or current_date
    check_out = data['check_out_time']

    if check_in < current_date:
        raise AttributeError(
            'Oops, a data do Check-In não pode inferior a data actual.')

    if check_in > check_out:
        raise AttributeError(
            'Oops, a data do Check-In não pode superior a data do Check-Out.')


def _valid_available_room(data):
    room = get(Room, int(data['room']))
    if room.status != 'available':
        raise AttributeError(
            'Oops, o quarto se encontra no estado {}.'.format(room.get_status_label()))


def validate_company(data: Dict[str, str]):
    for validator in [_valid_phone, _valid_cell, _valid_fax, _valid_nuit]:
        validator(data)


def validate_guest(data: Dict[str, str]):
    for validator in [_valid_cell]:
        validator(data)


def validate_reservation(data: Dict[str, str]):
    for validator in [_valid_date]:
        validator(data)


def validate_check_in(data: Dict[str, str]):
    for validator in [_valid_date, _valid_available_room]:
        validator(data)
