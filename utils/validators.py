from re import compile
from typing import Dict
from datetime import datetime

from peewee import Model
from wtforms.validators import DataRequired, Email

from dao import get
from models import Room


REQUIRED = DataRequired(message="Campo obrigatório.")
EMAIL = Email(message="Email inválido.")


def _valid_phone(obj):
    ''' valida o número do telefone '''
    regex = compile('^\\+258[0-9]{9}$')
    if not regex.match(obj.telephone):
        raise AttributeError(
            'Oops, o número do telefone é inválido (deve possuir o formato: +258XXXXXXXXX).')


def _valid_cell(obj):
    ''' valida o número do celular '''
    regex = compile('^\\+258[0-9]{9}$')
    if not regex.match(obj.cellphone):
        raise AttributeError(
            'Oops, o número do celular é inválido (deve possuir o formato: +258XXXXXXXXX).')


def _valid_fax(obj):
    ''' valida o número do fax '''
    regex = compile('^\\+258[0-9]{9}$')
    if not regex.match(obj.fax):
        raise AttributeError(
            'Oops, o número do fax é inválido (deve possuir o formato: +258XXXXXXXXX).')


def _valid_nuit(obj):
    ''' valida o NUIT '''
    regex = compile('^[1-9][0-9]{8}$')
    if not regex.match(obj.nuit):
        raise AttributeError('Oops, o NUIT é inválido.')


def _valid_check_in_date(obj):
    ''' a data do check in não pode ser superior da data actual '''
    if obj.check_in_time < datetime.now().date():
        raise AttributeError(
            'Oops, a data do Check-in não pode ser inferior a data actual.')


def _valid_check_out_date(obj):
    ''' a data do check in não pode ser superior da data do check out '''
    if obj.check_in_time >= obj.check_out_time:
        raise AttributeError(
            'Oops, a data do Check-out deve ser superior a data do Check-in.')


def _valid_available_room(obj):
    ''' verifica se o quarto está disponível '''
    room = get(Room, obj.room.id)
    if room.status != 'available':
        raise AttributeError(
            f'Oops, o quarto {room.number} se encontra no estado {room.get_status_label()}.')


def _valid_guest(obj):
    ''' o hóspede deve ser informado '''
    if obj.guest is None:
        raise AttributeError('O hóspede não foi informado')


def _valid_room_type(obj):
    ''' o tipo de quarto deve ser informado '''
    if obj.category is None:
        raise AttributeError('O Tipo de quarto não foi informado')


def validate_company(obj):
    ''' valida a empresa '''
    for validator in [_valid_phone, _valid_cell, _valid_fax, _valid_nuit]:
        validator(obj)


def validate_guest(obj):
    ''' valida a hóspede '''
    for validator in [_valid_cell]:
        validator(obj)


def validate_reservation(obj):
    ''' valida a reserva '''
    for validator in [_valid_check_in_date, _valid_check_out_date]:
        validator(obj)


def validate_check_in_creation(obj):
    ''' valida a criação do check in '''
    for validator in [_valid_check_in_date, _valid_check_out_date, _valid_available_room, ]:
        validator(obj)


def validate_check_in_edit(obj):
    ''' valida a alteração do check in '''
    for validator in [_valid_check_out_date, _valid_available_room, ]:
        validator(obj)


def validate_check_in_guest(obj):
    ''' valida a criação do hóspede no check in '''
    for validator in [_valid_guest]:
        validator(obj)


def validate_room(obj):
    ''' valida o quarto '''
    for validator in [_valid_room_type]:
        validator(obj)
