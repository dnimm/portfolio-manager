import pytest

from app.db import db
from app.models import User, Portfolio, Investment, Security
from app.service import trade_service


@pytest.fixture
def setup(db_session):
    u = User(username="u1", password="x", firstname="F", lastname="L", balance=1000.0)
    db.session.add(u)
    db.session.flush()

    p = Portfolio(name="P1", description="D1", owner=u.username, user=u)
    db.session.add(p)
    db.session.flush()

    return {"user": u, "portfolio": p}


def test_buy_trade_invalid_params():
    with pytest.raises(trade_service.TradeExecutionException):
        trade_service.buy_trade(None, "AAPL", 1)
    with pytest.raises(trade_service.TradeExecutionException):
        trade_service.buy_trade(1, "", 1)
    with pytest.raises(trade_service.TradeExecutionException):
        trade_service.buy_trade(1, "AAPL", 0)


def test_buy_trade_success_creates_security_and_investment(setup, monkeypatch, db_session):
    class Quote:
        ticker = "AAPL"
        issuer = "Apple Inc"
        price = 150.0
        date = "2026-03-08"

    monkeypatch.setattr("app.service.trade_service.get_quote", lambda t: Quote)

    p = setup["portfolio"]
    u = setup["user"]

    trade_service.buy_trade(p.id, "AAPL", 2)
    db.session.flush()

    db.session.refresh(u)
    assert u.balance == 700.0

    inv = next((x for x in p.investments if x.ticker == "AAPL"), None)
    assert inv is not None
    assert inv.quantity == 2

    sec = db.session.query(Security).filter_by(ticker="AAPL").one()
    assert sec.price == 150.0


def test_sell_trade_success_partial_and_full(setup, monkeypatch, db_session):
    class Quote:
        ticker = "AAPL"
        issuer = "Apple Inc"
        price = 150.0
        date = "2026-03-08"

    monkeypatch.setattr("app.service.trade_service.get_quote", lambda t: Quote)

    p = setup["portfolio"]
    u = setup["user"]

    
    trade_service.buy_trade(p.id, "AAPL", 4)
    db.session.flush()
    db.session.refresh(u)
    assert u.balance == 400.0

    
    trade_service.sell_trade(p.id, "AAPL", 1)
    db.session.flush()
    db.session.refresh(u)
    assert u.balance == 550.0
    inv = next(x for x in p.investments if x.ticker == "AAPL")
    assert inv.quantity == 3

    
    trade_service.sell_trade(p.id, "AAPL", 3)
    db.session.flush()
    db.session.refresh(u)
    assert u.balance == 1000.0
    assert all(x.ticker != "AAPL" for x in p.investments)


def test_sell_trade_errors(setup):
    p = setup["portfolio"]

    with pytest.raises(trade_service.TradeExecutionException):
        trade_service.sell_trade(p.id, "AAPL", 1)  