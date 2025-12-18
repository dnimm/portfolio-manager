from portfolioapp.database import db
from portfolioapp.domain.user import User
from sqlalchemy import select

def get_user_by_username(username: str):
    """Return a user object by username."""
    try:
        session = db.session
        user = session.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()
        return user
    except Exception as e:
        return None
