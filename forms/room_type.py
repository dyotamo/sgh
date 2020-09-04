from flask_wtf import FlaskForm
from wtforms import TextField

from utils.validators import REQUIRED


class RoomTypeForm(FlaskForm):
    name = TextField('Nome', validators=[REQUIRED])
