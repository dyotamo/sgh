from models import Room
from wtfpeewee.orm import model_form


RoomForm = model_form(Room, field_args={'number': dict(label='Número'),
                                        'category': dict(label='Tipo'),
                                        'daily_amount': dict(label='Valor da Diária')})
