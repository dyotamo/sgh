from wtfpeewee.orm import model_form
from models import Company


CompanyForm = model_form(Company, field_args={'name': dict(label='Nome'),
                                              'nuit': dict(label='NUIT'),
                                              'activity_branch': dict(label='Sector de Actuação'),
                                              'address': dict(label='Endereço'),
                                              'telephone': dict(label='Telefone'),
                                              'fax': dict(label='Fax'),
                                              'cellphone': dict(label='Celular')})
