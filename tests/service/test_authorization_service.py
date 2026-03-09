import pytest

from app.db import db
from app.models import User, Portfolio, PortfolioAccess
from app.service.authorization_service import AuthorizationError, check_portfolio_access


class FakeAuthUser:
    def __init__(self, username: str):
        self.username = username


@pytest.fixture
def setup(db_session):
    owner = User(username="owner", password="x", firstname="O", lastname="W", balance=1000)
    viewer = User(username="viewer", password="x", firstname="V", lastname="W", balance=1000)
    manager = User(username="manager", password="x", firstname="M", lastname="W", balance=1000)

    db.session.add_all([owner, viewer, manager])
    db.session.flush()

    p = Portfolio(name="P", description="D", owner=owner.username, user=owner)
    db.session.add(p)
    db.session.flush()

    db.session.add_all([
        PortfolioAccess(portfolio_id=p.id, username=viewer.username, role="viewer"),
        PortfolioAccess(portfolio_id=p.id, username=manager.username, role="manager"),
    ])
    db.session.flush()

    return {"owner": owner, "viewer": viewer, "manager": manager, "portfolio": p}


def test_owner_has_manager_access(setup):
    assert check_portfolio_access(FakeAuthUser("owner"), setup["portfolio"], "manager") is True


def test_viewer_has_viewer_access(setup):
    assert check_portfolio_access(FakeAuthUser("viewer"), setup["portfolio"], "viewer") is True


def test_viewer_denied_manager_access(setup):
    with pytest.raises(AuthorizationError):
        check_portfolio_access(FakeAuthUser("viewer"), setup["portfolio"], "manager")


def test_manager_has_manager_access(setup):
    assert check_portfolio_access(FakeAuthUser("manager"), setup["portfolio"], "manager") is True