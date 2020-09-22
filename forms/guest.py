from wtfpeewee.orm import model_form
from models import Guest


GuestForm = model_form(Guest, field_args={'name': dict(label='Nome'),
                                          'age': dict(label='Idade'),
                                          'id_type': dict(label='Tipo de Documento'),
                                          'id_number': dict(label='Número'),
                                          'address': dict(label='Endereço'),
                                          'cellphone': dict(label='Celular'),
                                          'father_name': dict(label='Nome do Pai'),
                                          'mother_name': dict(label='Nome da Mãe'),
                                          'marital_status': dict(label='Estado Civil'),
                                          'nationality': dict(label='Nacionalidade'),
                                          'company': dict(label='Em nome de'),
                                          'gender': dict(label='Gênero')})
