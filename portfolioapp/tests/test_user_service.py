from portfolioapp.domain.user import User
import portfolioapp.database as database
from rich.table import Table
import pytest
from portfolioapp.services.user_service import (
    get_all_users,
    build_users_table,
    create_user,
    delete_user,
)
from portfolioapp.session_state import set_logged_in_user, clear_logged_in_user
from portfolioapp.domain.portfolio import Portfolio

def test_insert_user_record(db_session):
    user = User(
        username="abc",
        password="pw",
        firstname="Test",
        lastname="User",
        balance=100.0
    )
    db_session.add(user)
    db_session.commit()
    result = db_session.query(User).filter_by(username="abc").one_or_none()
    assert result is not None


def test_get_all_users(db_session):
    users = get_all_users()
    assert isinstance(users, list)


def test_build_users_table(db_session):
    u = User(
        username="testuser",
        firstname="Test",
        lastname="User",
        password="password123",
        balance=1000.0
    )
    db_session.add(u)
    db_session.commit()
    users = get_all_users()
    t = build_users_table(users)
    assert isinstance(t, Table)



def test_create_user_success(monkeypatch, db_session):
    inputs = iter(["Alice", "Smith", "aliceX", "pw", "500"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    msg = create_user()
    assert "success" in msg.lower()  




def test_delete_user_success(monkeypatch, db_session):
    u = User(username="delme", firstname="D", lastname="U", password="pw", balance=50)
    db_session.add(u)
    db_session.commit()

    monkeypatch.setattr("builtins.input", lambda *args: "delme")
    msg = delete_user()
    assert "success" in msg.lower()


def test_delete_user_not_found(monkeypatch, db_session):
    monkeypatch.setattr("builtins.input", lambda *args: "nouser")
    with pytest.raises(Exception):
        delete_user()


def test_delete_user_cannot_delete_admin(monkeypatch, db_session):
    monkeypatch.setattr("builtins.input", lambda *args: "admin")
    with pytest.raises(Exception):
        delete_user()





def test_delete_user_with_portfolios(monkeypatch, db_session):
    u = User(username="pfuser", firstname="PF", lastname="Owner", password="pw", balance=100)
    db_session.add(u)
    db_session.commit()

    p = Portfolio(name="P1", description="d", owner_username="pfuser")
    db_session.add(p)
    db_session.commit()

    monkeypatch.setattr("builtins.input", lambda *args: "pfuser")

    with pytest.raises(Exception):
        delete_user()




