import pytest
from flask import g

from app.db import db
from app.models import User, Portfolio, PortfolioAccess
from app.routes import portfolio_routes


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
def viewer(db_session):
    u = User(username="viewer", password="x", firstname="V", lastname="W", balance=1000.0)
    db.session.add(u)
    db.session.flush()
    return u


@pytest.fixture
def portfolio(db_session, owner):
    p = Portfolio(name="P1", description="D1", owner=owner.username, user=owner)
    db.session.add(p)
    db.session.flush()
    return p


def test_get_portfolio_allowed_with_viewer_access(app, db_session, portfolio, viewer):
    db.session.add(PortfolioAccess(portfolio_id=portfolio.id, username=viewer.username, role="viewer"))
    db.session.commit()

    fn = _unwrap(portfolio_routes.get_portfolio)

    with app.test_request_context(f"/portfolios/{portfolio.id}"):
        g.current_user = {"username": viewer.username}
        resp, status = fn(portfolio.id)

    assert status == 200
    assert resp.get_json()["id"] == portfolio.id


def test_get_portfolio_forbidden_without_access(app, portfolio):
    fn = _unwrap(portfolio_routes.get_portfolio)

    with app.test_request_context(f"/portfolios/{portfolio.id}"):
        g.current_user = {"username": "no_access_user"}
        resp, status = fn(portfolio.id)

    assert status == 403


def test_create_portfolio_success(app, db_session, owner):
    fn = _unwrap(portfolio_routes.create_portfolio)

    with app.test_request_context(
        "/portfolios/",
        method="POST",
        json={"username": owner.username, "name": "New", "description": "Desc"},
    ):
        g.current_user = {"username": owner.username}
        resp, status = fn()

    assert status == 201
    body = resp.get_json()
    assert "id" in body

    
    created = db.session.query(Portfolio).filter_by(id=body["id"]).one()
    assert created.owner == owner.username


def test_create_portfolio_forbidden_for_other_username(app, owner):
    fn = _unwrap(portfolio_routes.create_portfolio)

    with app.test_request_context(
        "/portfolios/",
        method="POST",
        json={"username": "someone_else", "name": "X", "description": "Y"},
    ):
        g.current_user = {"username": owner.username}
        resp, status = fn()

    assert status == 403