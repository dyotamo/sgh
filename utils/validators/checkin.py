from datetime import datetime

from dao import get
from models import Room


def valid_check_in_date(obj):
    ''' a data do check in não pode ser inferior da data actual '''
    if obj.check_in_time < datetime.now().date():
        raise AttributeError(
            'Oops, a data do Check-in não pode ser inferior a data actual.')


def valid_check_out_date(obj):
    ''' a data do check in não pode ser superior da data do check out '''
    if obj.check_in_time >= obj.check_out_time:
        raise AttributeError(
            'Oops, a data do Check-out deve ser superior a data do Check-in.')


def valid_available_room(obj):
    ''' verifica se o quarto está disponível '''
    room = get(Room, obj.room.id)
    if room.status != 'available':
        raise AttributeError(
            f'Oops, o quarto {room.number} se encontra no etado {room.get_status_label()}.')


def valid_guest(obj):
    ''' o hóspede deve ser informado '''
    if obj.guest is None:
        raise AttributeError('O hóspede não foi informado')


def validate_check_in_creation(obj):
    ''' valida a criação do check in '''
    for validator in [valid_check_in_date, valid_check_out_date, valid_available_room, ]:
        validator(obj)


def validate_check_in_edit(obj):
    ''' valida a alteração do check in '''
    for validator in [valid_check_out_date, valid_available_room, ]:
        validator(obj)


def validate_check_in_guest(obj):
    ''' valida a criação do hóspede no check in '''
    for validator in [valid_guest]:
        validator(obj)
