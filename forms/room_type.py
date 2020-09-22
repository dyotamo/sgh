from wtfpeewee.orm import model_form
from models import RoomType


RoomTypeForm = model_form(RoomType, field_args={'name': dict(label='Tipo')})
