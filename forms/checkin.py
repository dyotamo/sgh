from wtfpeewee.orm import model_form
from models import CheckIn, CheckInGuest


CheckInForm = model_form(CheckIn, field_args={'room': dict(label='Quarto'),
                                              'check_out_time': dict(label='Data do Check-out')})

CheckInGuestForm = model_form(CheckInGuest, field_args={
                              'guest': dict(label='Hóspede')})
