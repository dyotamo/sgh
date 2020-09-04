from typing import Dict
from flask_wtf import FlaskForm

from models import Company
from dao import get_all


def get_formdata(form: FlaskForm) -> Dict[str, str]:
    data = form.data
    data.pop('csrf_token')
    return data


def get_model_tuple(model):
    return [(str(obj.id), obj.name) for obj in get_all(model)]
