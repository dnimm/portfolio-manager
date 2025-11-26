import pytest
from portfolioapp.domain.user import User
from portfolioapp.domain.portfolio import Portfolio
from portfolioapp.domain.security import Security
from portfolioapp.domain.investment import Investment
from portfolioapp.services.portfolio_service import (
    get_all_portfolios,
    build_portfolio_table,
    create_portfolio,
    delete_portfolio,
    buy_security,
    sell_security
)
import portfolioapp.database as database



def create_test_user(db_session, username="testuser", bal=1000):
    u = User(
        username=username,
        firstname="Test",
        lastname="User",
        password="pw",
        balance=bal
    )
    db_session.add(u)
    db_session.commit()
    return u


def create_test_security(db_session, ticker="AAA", price=10):
    s = Security(ticker=ticker, issuer="Corp", price=price)
    db_session.add(s)
    db_session.commit()
    return s


def create_test_portfolio(db_session, user, name="P1"):
    p = Portfolio(
        name=name,
        description="desc",
        owner_username=user.username
    )
    db_session.add(p)
    db_session.commit()
    return p



def test_get_all_portfolios_empty(db_session):
    import portfolioapp.services.portfolio_service as ps
    import portfolioapp.database as db

    
    ps.get_session = lambda: db_session
    db.get_session = lambda: db_session
    ps.database.get_session = lambda: db_session

    
    db_session.query(Portfolio).delete()
    db_session.commit()

    assert get_all_portfolios() == []



def test_get_all_portfolios_with_items(db_session):
    database.get_session = lambda: db_session
    u = create_test_user(db_session, "owner1")
    p = create_test_portfolio(db_session, u, "TestPF")
    results = get_all_portfolios()
    assert len(results) == 1
    assert results[0].name == "TestPF"




def test_create_portfolio_success(monkeypatch, db_session):
    database.get_session = lambda: db_session
    create_test_user(db_session, "gooduser")

    inputs = iter(["MyPF", "gooduser", "A test pf"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    msg = create_portfolio()
    assert "created" in msg.lower()


def test_create_portfolio_invalid_user(monkeypatch, db_session):
    database.get_session = lambda: db_session

    inputs = iter(["MyPF", "NOUSER", "desc"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    msg = create_portfolio()
    assert "not found" in msg.lower()




def test_delete_portfolio_success(monkeypatch, db_session):
    database.get_session = lambda: db_session
    u = create_test_user(db_session, "deluser")
    p = create_test_portfolio(db_session, u, "PFDEL")

    monkeypatch.setattr("builtins.input", lambda *args: str(p.id))
    msg = delete_portfolio()
    assert "deleted" in msg.lower()


def test_delete_portfolio_not_found(monkeypatch, db_session):
    database.get_session = lambda: db_session

    monkeypatch.setattr("builtins.input", lambda *args: "999")
    msg = delete_portfolio()
    assert "not found" in msg.lower()


def test_delete_portfolio_has_holdings(monkeypatch, db_session):
    database.get_session = lambda: db_session

    u = create_test_user(db_session, "holduser")
    p = create_test_portfolio(db_session, u, "PFHOLD")

    inv = Investment(
        portfolio_id=p.id,
        ticker="AAA",
        quantity=5,
        purchase_price=10
    )
    db_session.add(inv)
    db_session.commit()

    monkeypatch.setattr("builtins.input", lambda *args: str(p.id))
    msg = delete_portfolio()
    assert "holdings" in msg.lower()




def test_buy_security_success(monkeypatch, db_session):
    database.get_session = lambda: db_session

    u = create_test_user(db_session, "buyer", 500)
    p = create_test_portfolio(db_session, u)
    create_test_security(db_session, "ABCD", 20)

    inputs = iter([str(p.id), "ABCD", "2"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    msg = buy_security()
    assert "completed" in msg.lower()


def test_buy_security_invalid_portfolio(monkeypatch, db_session):
    database.get_session = lambda: db_session

    inputs = iter(["999", "ABC", "1"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    msg = buy_security()
    assert "invalid" in msg.lower()


def test_buy_security_invalid_ticker(monkeypatch, db_session):
    database.get_session = lambda: db_session

    u = create_test_user(db_session, "buyer2")
    p = create_test_portfolio(db_session, u)

    inputs = iter([str(p.id), "FAKE", "2"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    msg = buy_security()
    assert "invalid" in msg.lower()


def test_buy_security_insufficient_balance(monkeypatch, db_session):
    database.get_session = lambda: db_session

    u = create_test_user(db_session, "poor", 1)
    p = create_test_portfolio(db_session, u)
    create_test_security(db_session, "HIGH", 999)

    inputs = iter([str(p.id), "HIGH", "1"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    msg = buy_security()
    assert "insufficient" in msg.lower()




def test_sell_security_success(monkeypatch, db_session):
    database.get_session = lambda: db_session

    u = create_test_user(db_session, "seller")
    p = create_test_portfolio(db_session, u)
    create_test_security(db_session, "SELL", 10)

    inv = Investment(
        portfolio_id=p.id,
        ticker="SELL",
        quantity=5,
        purchase_price=10
    )
    db_session.add(inv)
    db_session.commit()

    inputs = iter([str(p.id), "SELL", "3", "15"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    msg = sell_security()
    assert "completed" in msg.lower()


def test_sell_security_invalid_port(monkeypatch, db_session):
    database.get_session = lambda: db_session

    inputs = iter(["999", "AAA", "1", "10"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    msg = sell_security()
    assert "invalid" in msg.lower()


def test_sell_security_not_found(monkeypatch, db_session):
    database.get_session = lambda: db_session

    u = create_test_user(db_session, "seller2")
    p = create_test_portfolio(db_session, u)

    inputs = iter([str(p.id), "FAKE", "1", "10"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    msg = sell_security()
    assert "not found" in msg.lower()


def test_sell_security_not_enough_qty(monkeypatch, db_session):
    database.get_session = lambda: db_session

    u = create_test_user(db_session, "lowshares")
    p = create_test_portfolio(db_session, u)
    create_test_security(db_session, "LMT", 10)

    inv = Investment(
        portfolio_id=p.id,
        ticker="LMT",
        quantity=1,
        purchase_price=10
    )
    db_session.add(inv)
    db_session.commit()

    inputs = iter([str(p.id), "LMT", "5", "10"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    msg = sell_security()
    assert "not enough" in msg.lower()
