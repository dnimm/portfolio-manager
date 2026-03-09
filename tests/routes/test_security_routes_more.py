import uuid
from flask import g

from app.db import db
from app.models import Security, Transaction, User, Portfolio
from app.routes import security_routes


def _unwrap(fn):
    while hasattr(fn, "__wrapped__"):
        fn = fn.__wrapped__
    return fn


def _set_auth():
    g.current_user = {"username": "testuser"}


def _u(prefix="x"):
    return f"{prefix}_{uuid.uuid4().hex[:10]}"





def test_get_security_not_found(app, monkeypatch):
    monkeypatch.setattr("app.service.security_service.get_security_by_ticker", lambda t: None)

    fn = _unwrap(security_routes.get_security)
    with app.test_request_context("/securities/No"):
        _set_auth()
        resp, status = fn("No")

    assert status == 404


def test_get_security_transactions(app, db_session):
    
    username = _u("u")
    u = User(username=username, password="x", firstname="F", lastname="L", balance=1000.0)
    db.session.add(u)
    db.session.flush()

    p = Portfolio(name=_u("p"), description="D", owner=username, user=u)
    db.session.add(p)
    db.session.flush()

    db.session.add(Transaction(
        portfolio_id=p.id,
        username=username,
        ticker="AAPL",
        quantity=2,
        price=150.0,
        transaction_type="BUY",
    ))
    db.session.commit()

    fn = _unwrap(security_routes.get_security_transactions)
    with app.test_request_context("/securities/AAPL/transactions"):
        _set_auth()
        resp, status = fn("AAPL")

    assert status == 200
    body = resp.get_json()
    assert len(body) >= 1
    assert body[0]["ticker"] == "AAPL"