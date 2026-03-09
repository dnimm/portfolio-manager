import pytest

from app.service import security_service


def test_get_security_by_ticker_returns_quote(monkeypatch):
    class FakeQuote:
        ticker = "AAPL"
        issuer = "Apple Inc."
        price = 123.45
        date = "2026-03-06"

    monkeypatch.setattr(security_service, "get_quote", lambda _ticker: FakeQuote())

    q = security_service.get_security_by_ticker("AAPL")
    assert q is not None
    assert q["ticker"] == "AAPL"
    assert q["issuer"] == "Apple Inc."
    assert q["price"] == 123.45
    assert q["date"] == "2026-03-06"


def test_get_security_by_ticker_not_found(monkeypatch):
    monkeypatch.setattr(security_service, "get_quote", lambda _ticker: None)
    q = security_service.get_security_by_ticker("INVALID")
    assert q is None


def test_get_all_securities_returns_db_rows(db_session):
    
    secs = security_service.get_all_securities()
    assert isinstance(secs, list)
   