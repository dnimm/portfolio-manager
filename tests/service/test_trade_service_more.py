import pytest
from app.db import db
from app.models import User, Portfolio, Security
from app.service import trade_service


@pytest.fixture
def setup(db_session):
    u = User(username="u", password="x", firstname="F", lastname="L", balance=1000.0)
    db.session.add(u)
    db.session.flush()
    p = Portfolio(name="P", description="D", owner=u.username, user=u)
    db.session.add(p)
    db.session.flush()
    return u, p


def test_buy_trade_invalid_params_raises(db_session):
    with pytest.raises(trade_service.TradeExecutionException):
        trade_service.buy_trade(None, "AAPL", 1)
    with pytest.raises(trade_service.TradeExecutionException):
        trade_service.buy_trade(1, "", 1)
    with pytest.raises(trade_service.TradeExecutionException):
        trade_service.buy_trade(1, "AAPL", 0)


def test_buy_trade_insufficient_funds(db_session, setup, monkeypatch):
    u, p = setup
    u.balance = 1.0
    db.session.flush()

    class Quote:
        ticker = "AAPL"
        issuer = "Apple"
        price = 150.0
        date = "2026-03-08"

    monkeypatch.setattr("app.service.trade_service.get_quote", lambda t: Quote)

    with pytest.raises(trade_service.InsufficientFundsError):
        trade_service.buy_trade(p.id, "AAPL", 1)


def test_buy_trade_success_creates_security_investment_and_txn(db_session, setup, monkeypatch):
    u, p = setup

    class Quote:
        ticker = "AAPL"
        issuer = "Apple"
        price = 150.0
        date = "2026-03-08"

    monkeypatch.setattr("app.service.trade_service.get_quote", lambda t: Quote)

    trade_service.buy_trade(p.id, "AAPL", 2)
    db.session.flush()

    assert u.balance == 700.0
    assert len(p.investments) == 1
    assert p.investments[0].ticker == "AAPL"
    assert p.investments[0].quantity == 2

    
    s = db.session.query(Security).filter_by(ticker="AAPL").one()
    assert s.price == 150.0
    assert s.issuer == "Apple"