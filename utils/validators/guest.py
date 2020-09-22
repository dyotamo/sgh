from .company import valid_cell


def validate_guest(obj):
    ''' valida a hóspede '''
    for validator in [valid_cell]:
        validator(obj)
