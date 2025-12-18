from portfolioapp.db import db
from portfolioapp.domain.user import User

def get_all_users():
    return User.query.all()

def get_user(username):
    return User.query.get(username)

def create_user(data):
    if User.query.get(data["username"]):
        return None
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user

def delete_user(username):
    user = User.query.get(username)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True
