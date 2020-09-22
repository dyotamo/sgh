def valid_room_type(obj):
    ''' o tipo de quarto deve ser informado '''
    if obj.category is None:
        raise AttributeError('O tipo de quarto não foi informado')


def validate_room(obj):
    ''' valida o quarto '''
    for validator in [valid_room_type]:
        validator(obj)
