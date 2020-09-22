def valid_room_type(obj):
    ''' o tipo de quarto deve ser informado '''
    if obj.category is None:
        raise AttributeError('O Tipo de quarto não foi informado')


def validate_room(obj):
    ''' valida o quarto '''
    for validator in [valid_room_type]:
        validator(obj)
