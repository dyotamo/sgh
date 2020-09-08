from werkzeug.security import check_password_hash
from models import User


def toogle_activation(obj):
    obj.is_active = not obj.is_active
    obj.save()
    return obj


def check_user(email, password):
    try:
        user = User.get(User.email == email)
        if check_password_hash(user.password, password):
            return user
    except User.DoesNotExist:
        pass
