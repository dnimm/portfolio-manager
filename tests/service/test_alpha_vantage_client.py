import pytest
from flask import Flask

from app.cache import cache
from app.service import alpha_vantage_client as av


@pytest.fixture()
def flask_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["ALPHAVANTAGE_API_KEY"] = "fake_key"
    cache.init_app(app)
    return app


def test_get_company_name_success(monkeypatch, flask_app):
    class FakeResp:
        def raise_for_status(self): ...
        def json(self):
            return {"Name": "Apple Inc."}

    def fake_get(*args, **kwargs):
        return FakeResp()

    with flask_app.app_context():
        monkeypatch.setattr(av.requests, "get", fake_get)
        assert av.get_company_name("AAPL") == "Apple Inc."


def test_get_company_name_none_when_missing(monkeypatch, flask_app):
    class FakeResp:
        def raise_for_status(self): ...
        def json(self):
            return {}

    def fake_get(*args, **kwargs):
        return FakeResp()

    with flask_app.app_context():
        monkeypatch.setattr(av.requests, "get", fake_get)
        assert av.get_company_name("XXXX") is None


def test_cache_skips_http_call_for_company_name(monkeypatch, flask_app):
    called = {"count": 0}

    def fake_get(*args, **kwargs):
        called["count"] += 1
        raise AssertionError("requests.get should not be called when cached")

    with flask_app.app_context():
        cache.set("company_name:AAPL", "Apple Inc.")
        monkeypatch.setattr(av.requests, "get", fake_get)
        assert av.get_company_name("AAPL") == "Apple Inc."
        assert called["count"] == 0


def test_get_price_data_success(monkeypatch, flask_app):
    class FakeResp:
        def raise_for_status(self): ...
        def json(self):
            return {
                "Time Series (Daily)": {
                    "2026-03-06": {
                        "1. open": "10",
                        "2. high": "12",
                        "3. low": "9",
                        "4. close": "11",
                        "5. volume": "1000",
                    }
                }
            }

    def fake_get(*args, **kwargs):
        return FakeResp()

    with flask_app.app_context():
        monkeypatch.setattr(av.requests, "get", fake_get)
        data = av.get_price_data("AAPL")
        assert data["date"] == "2026-03-06"
        assert data["close"] == 11.0


def test_get_quote_returns_none_when_partial(monkeypatch, flask_app):
    
    class FakeOverviewResp:
        def raise_for_status(self): ...
        def json(self):
            return {"Name": "Apple Inc."}

    class FakePriceResp:
        def raise_for_status(self): ...
        def json(self):
            return {}

    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        return FakeOverviewResp() if calls["n"] == 1 else FakePriceResp()

    with flask_app.app_context():
        monkeypatch.setattr(av.requests, "get", fake_get)
        assert av.get_quote("AAPL") is None