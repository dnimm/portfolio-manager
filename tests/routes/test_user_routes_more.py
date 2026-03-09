import uuid
from flask import g

from app.db import db
from app.models import User, Transaction, Portfolio
from app.routes import user_routes


def _unwrap(fn):
    while hasattr(fn, "__wrapped__"):
        fn = fn.__wrapped__
    return fn


def _set_auth():
    
    g.current_user = {"username": "testuser"}


def _u(prefix="u"):
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def test_get_users(app, db_session):
    
    username = _u("u")
    db.session.add(User(username=username, password="pw", firstname="F", lastname="L", balance=1000.0))
    db.session.commit()

    fn = _unwrap(user_routes.get_users)
    with app.test_request_context("/users/"):
        _set_auth()
        resp, status = fn()

    assert status == 200
    body = resp.get_json()
    assert isinstance(body, list)
    assert any(x["username"] == username for x in body)


def test_get_user_not_found(app):
    fn = _unwrap(user_routes.get_user)
    with app.test_request_context("/users/nope"):
        _set_auth()
        resp, status = fn("nope")
    assert status == 404


def test_create_user_success(app, db_session):
    fn = _unwrap(user_routes.create_user)

    username = _u("new")
    with app.test_request_context(
        "/users/",
        method="POST",
        json={"username": username, "password": "x", "firstname": "A", "lastname": "B", "balance": 123.0},
    ):
        _set_auth()
        resp, status = fn()

    assert status == 201
    assert resp.get_json()["message"] == "User created successfully"
    assert db.session.query(User).filter_by(username=username).one_or_none() is not None


def test_update_balance_success(app, db_session):
    username = _u("bal")
    db.session.add(User(username=username, password="x", firstname="F", lastname="L", balance=10.0))
    db.session.commit()

    fn = _unwrap(user_routes.update_balance)
    with app.test_request_context(
        "/users/update-balance",
        method="PUT",
        json={"username": username, "new_balance": 777.0},
    ):
        _set_auth()
        resp, status = fn()

    assert status == 200
    u = db.session.query(User).filter_by(username=username).one()
    assert u.balance == 777.0


def test_delete_user_success(app, db_session):
    username = _u("del")
    db.session.add(User(username=username, password="x", firstname="T", lastname="D", balance=1.0))
    db.session.commit()

    fn = _unwrap(user_routes.delete_user)
    with app.test_request_context(f"/users/{username}", method="DELETE"):
        _set_auth()
        resp, status = fn(username)

    assert status == 200
    assert db.session.query(User).filter_by(username=username).one_or_none() is None


def test_get_user_transactions(app, db_session):
    username = _u("txn")
    u = User(username=username, password="x", firstname="F", lastname="L", balance=1000.0)
    db.session.add(u)
    db.session.flush()

    p = Portfolio(name=_u("p"), description="D", owner=username, user=u)
    db.session.add(p)
    db.session.flush()

    t = Transaction(
        portfolio_id=p.id,
        username=username,
        ticker="AAPL",
        quantity=1,
        price=150.0,
        transaction_type="BUY",
    )
    db.session.add(t)
    db.session.commit()

    fn = _unwrap(user_routes.get_user_transactions)
    with app.test_request_context(f"/users/{username}/transactions"):
        _set_auth()
        resp, status = fn(username)

    assert status == 200
    body = resp.get_json()
    assert len(body) == 1
    assert body[0]["ticker"] == "AAPL"