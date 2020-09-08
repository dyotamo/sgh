from typing import Dict
from flask_wtf import FlaskForm

from dao import get_all


def get_formdata(form: FlaskForm) -> Dict[str, str]:
    data = form.data
    data.pop('csrf_token')
    return data


# Using introspection
def get_model_tuple(model, attr='name'):
    return [(str(obj.id), getattr(obj, attr)) for obj in get_all(model)]
