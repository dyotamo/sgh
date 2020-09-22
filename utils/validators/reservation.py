from .checkin import valid_check_in_date, valid_check_out_date


def validate_reservation(obj):
    ''' valida a reserva '''
    for validator in [valid_check_in_date, valid_check_out_date]:
        validator(obj)
