import pytest
from portfolioapp.domain.user import User
import portfolioapp.session_state as session_state
import portfolioapp.database as database
from portfolioapp.services.login_service import login, logout



def patch_sessions(db_session):
    import portfolioapp.services.login_service as ls

    
    ls.get_session = lambda: db_session
    database.get_session = lambda: db_session




def test_login_success(monkeypatch, db_session):
    patch_sessions(db_session)

    # create user
    user = User(
        username="john",
        firstname="John",
        lastname="Doe",
        password="pass123",
        balance=1000
    )
    db_session.add(user)
    db_session.commit()

    
    inputs = iter(["john", "pass123"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    
    login()

    
    logged_in = session_state.get_logged_in_user()
    assert logged_in is not None
    assert logged_in.username == "john"



def test_logout_clears_user(db_session):
    patch_sessions(db_session)

    
    fake_user = User(
        username="x",
        firstname="Temp",
        lastname="User",
        password="pw",
        balance=100
    )
    session_state.set_logged_in_user(fake_user)

    logout()

    assert session_state.get_logged_in_user() is None
