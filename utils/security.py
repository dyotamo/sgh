from functools import wraps

from flask import abort
from flask_login import current_user


class allowed_profile:
    def __init__(self, profiles):
        self.profiles = profiles

    def __call__(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            user_authed = current_user.is_authenticated
            if user_authed and current_user.profile in self.profiles:
                return func(*args, **kwargs)
            raise abort(403)
        return wrapped_func
