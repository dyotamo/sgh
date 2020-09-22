from flask import abort
from peewee import fn


def get(model, id: int):
    try:
        return model.get(id)
    except model.DoesNotExist:
        abort(404)


def get_all(model):
    return model.select().order_by(model.id.desc())


def get_random(model):
    return model.select().order_by(fn.Random()).get()


def get_where(model, **kwargs):
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        pass


def create(model, **kwargs):
    model.create(**kwargs)


def delete(obj):
    obj.delete_instance()
