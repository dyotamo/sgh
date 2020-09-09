from datetime import datetime
from typing import Type

from flask import abort
from peewee import Model, ModelSelect, fn
from playhouse.shortcuts import update_model_from_dict


def get(model: Type, id: int) -> Model:
    try:
        return model.get(id)
    except model.DoesNotExist:
        raise abort(404)


def get_all(model: Type) -> ModelSelect:
    return model.select()


def get_random(model: Type) -> Model:
    return model.select().order_by(fn.Random()).get()


def get_where(model: Type, **kwargs) -> Model:
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        pass


def create(model: Type, **kwargs):
    model.create(**kwargs)


def update(model: Type, id: int, **kwargs):
    instance = get(model, id)
    _update_attrs(kwargs, instance)
    instance.save()
    return instance


def _update_attrs(kwargs, instance):
    """ that was tricky, using
    reflection to update newer attrs """
    for k, v in kwargs.items():
        setattr(instance, k, v)
