import pytest
from flask import g

from app.db import db
from app.models import User, Portfolio, PortfolioAccess
from app.routes import trade_routes


def _unwrap(fn):
    while hasattr(fn, "__wrapped__"):
        fn = fn.__wrapped__
    return fn


@pytest.fixture
def owner(db_session):
    u = User(username="owner", password="x", firstname="O", lastname="W", balance=1000.0)
    db.session.add(u)
    db.session.flush()
    return u


@pytest.fixture
def portfolio(db_session, owner):
    p = Portfolio(name="P1", description="D1", owner=owner.username, user=owner)
    db.session.add(p)
    db.session.flush()
    return p


def test_buy_forbidden_without_manager_access(app, portfolio):
    fn = _unwrap(trade_routes.buy)

    with app.test_request_context(
        "/trades/buy",
        method="POST",
        json={"portfolio_id": portfolio.id, "ticker": "AAPL", "quantity": 1},
    ):
        g.current_user = {"username": "not_owner"}
        resp, status = fn()

    assert status == 403


def test_buy_success_owner(app, db_session, portfolio, owner, monkeypatch):
    
    class Quote:
        ticker = "AAPL"
        issuer = "Apple Inc"
        price = 150.0
        date = "2026-03-08"

    monkeypatch.setattr("app.service.trade_service.get_quote", lambda t: Quote)

    fn = _unwrap(trade_routes.buy)

    with app.test_request_context(
        "/trades/buy",
        method="POST",
        json={"portfolio_id": portfolio.id, "ticker": "AAPL", "quantity": 2},
    ):
        g.current_user = {"username": owner.username}
        resp, status = fn()

    assert status == 201
    assert resp.get_json()["message"] == "buy order executed"