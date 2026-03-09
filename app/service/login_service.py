from app.models import User
from app.db import db


_current_user = None


class LoginError(Exception):
    pass


def login(username: str, password: str):
    global _current_user

    user = db.session.query(User).filter_by(username=username).one_or_none()

    if not user:
        raise LoginError("Invalid username")

    if user.password != password:
        raise LoginError("Invalid password")

    _current_user = user


def logout():
    global _current_user
    _current_user = None


def get_logged_in_user():
    return _current_user