from datetime import datetime
from typing import Type

from flask import abort
from flask_login import current_user
from peewee import Model, ModelSelect

from models import db


def get(model: Type, id: int) -> Model:
    try:
        return model.get(id)
    except model.DoesNotExist:
        raise abort(404)


def get_all(model: Type) -> ModelSelect:
    return model.select()


def get_where(model: Type, **kwargs) -> Model:
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        pass


@db.atomic()
def create(model: Type, **kwargs):
    obj = model.create(**kwargs)
    obj.created_by = current_user.id
    obj.save()


@db.atomic()
def update(model: Type, id: int, **kwargs):
    model.update(**kwargs).where(model.id == id).execute()
    obj = get(model, id)
    obj.updated_by = current_user.id
    obj.updated_at = datetime.now()
    obj.save()
