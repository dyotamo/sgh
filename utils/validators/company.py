from re import compile


def valid_phone(obj):
    ''' valida o número do telefone '''
    regex = compile('^\\+258[0-9]{9}$')
    if not regex.match(obj.telephone):
        raise AttributeError(
            'Oops, o número do telefone é inválido (deve possuir o formato: +258XXXXXXXXX).')


def valid_cell(obj):
    ''' valida o número do celular '''
    regex = compile('^\\+258[0-9]{9}$')
    if not regex.match(obj.cellphone):
        raise AttributeError(
            'Oops, o número do celular é inválido (deve possuir o formato: +258XXXXXXXXX).')


def valid_fax(obj):
    ''' valida o número do fax '''
    regex = compile('^\\+258[0-9]{9}$')
    if not regex.match(obj.fax):
        raise AttributeError(
            'Oops, o número do fax é inválido (deve possuir o formato: +258XXXXXXXXX).')


def valid_nuit(obj):
    ''' valida o NUIT '''
    regex = compile('^[1-9][0-9]{8}$')
    if not regex.match(obj.nuit):
        raise AttributeError('Oops, o NUIT é inválido.')


def validate_company(obj):
    ''' valida a empresa '''
    for validator in [valid_phone, valid_cell, valid_fax, valid_nuit]:
        validator(obj)
