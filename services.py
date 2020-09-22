from werkzeug.security import check_password_hash
from models import User


def check_user(email, password):
    try:
        user = User.get(User.email == email)
        if check_password_hash(user.password, password):
            return user
    except User.DoesNotExist:
        pass
