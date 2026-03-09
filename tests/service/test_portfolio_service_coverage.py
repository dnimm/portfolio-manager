import pytest
from app.service import portfolio_service
from app.models import User


def test_get_all_portfolios_db_failure(monkeypatch):
    monkeypatch.setattr("app.database.get_session", lambda: (_ for _ in ()).throw(Exception("Database connection error")))

    with pytest.raises(Exception) as e:
        portfolio_service.get_all_portfolios()

    
    assert "Database connection error" in str(e.value)


def test_get_portfolio_by_id_db_failure(monkeypatch):
    monkeypatch.setattr("app.database.get_session", lambda: (_ for _ in ()).throw(Exception("Database connection error")))

    with pytest.raises(Exception) as e:
        portfolio_service.get_portfolio_by_id(1)

    assert "Database connection error" in str(e.value)


def test_get_portfolios_by_user_db_failure(monkeypatch):
    monkeypatch.setattr("app.database.get_session", lambda: (_ for _ in ()).throw(Exception("Database connection error")))

    u = User(username="u1", password="x", firstname="F", lastname="L", balance=1.0)

    with pytest.raises(Exception) as e:
        portfolio_service.get_portfolios_by_user(u)

    assert "Database connection error" in str(e.value)