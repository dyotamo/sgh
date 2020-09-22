from functools import wraps

from werkzeug.security import check_password_hash
from flask import abort
from flask_login import current_user
from peewee import DoesNotExist

from models import User


class allowed_profile:
    def __init__(self, profiles):
        self.profiles = profiles

    def __call__(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if current_user.profile in self.profiles:
                return func(*args, **kwargs)
            abort(403)
        return wrapped_func


def check_user(email, password):
    try:
        user = User.get(User.email == email)
        if check_password_hash(user.password, password):
            return user
    except DoesNotExist:
        pass
