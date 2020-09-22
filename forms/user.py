from wtfpeewee.orm import model_form
from models import User


UserForm = model_form(User, field_args={'name': dict(
    label='Nome'), 'profile': dict(label='Perfil')})
