import pytest

from app.db import db
from app.models import User
from app.service import portfolio_service


@pytest.fixture
def user(db_session):
    u = User(username="user1", password="pw", firstname="F", lastname="L", balance=1000.0)
    db.session.add(u)
    db.session.flush()
    return u


def test_create_portfolio_success(user):
    pid = portfolio_service.create_portfolio("P1", "D1", user)
    assert isinstance(pid, int)


def test_create_portfolio_invalid_input(user):
    with pytest.raises(portfolio_service.UnsupportedPortfolioOperationError):
        portfolio_service.create_portfolio("", "D1", user)
    with pytest.raises(portfolio_service.UnsupportedPortfolioOperationError):
        portfolio_service.create_portfolio("P1", "", user)


def test_get_all_portfolios_returns_list(user):
    portfolio_service.create_portfolio("P1", "D1", user)
    db.session.flush()
    portfolios = portfolio_service.get_all_portfolios()
    assert isinstance(portfolios, list)
    assert len(portfolios) >= 1