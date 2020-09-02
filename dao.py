from datetime import datetime

from flask import abort
from flask_login import current_user

from models import db


def get(model, id):
    try:
        return model.get(id)
    except model.DoesNotExist:
        abort(404)


def get_all(model):
    return model.select()


def get_where(model, **kwargs):
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        pass


@db.atomic()
def create(model, **kwargs):
    obj = model.create(**kwargs)
    obj.created_by = current_user.id
    obj.save()


@db.atomic()
def update(model, id, **kwargs):
    model.update(**kwargs).where(model.id == id).execute()
    obj = get(model, id)
    obj.updated_by = current_user.id
    obj.updated_at = datetime.now()
    obj.save()
