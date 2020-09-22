from wtfpeewee.orm import model_form
from models import Reservation


ReservationForm = model_form(Reservation, field_args={'check_in_time': dict(label='Data do Check-in'),
                                                      'check_out_time': dict(label='Data do Check-out'),
                                                      'adult_number': dict(label='Adultos'),
                                                      'children_number': dict(label='Crianças'),
                                                      'company': dict(label='Em nome de')})
