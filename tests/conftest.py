from __future__ import annotations

import sys
from pathlib import Path
from typing import Generator

import pytest

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from app import create_app
from app.config import TestConfig
from app.db import db
from app.models import Security, User


@pytest.fixture(scope="function")
def app():
    flask_app = create_app(TestConfig)

    with flask_app.app_context():
        db.create_all()
        _populate_database()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app) -> Generator:
    yield db.session
    db.session.rollback()


def _populate_database():
    
    if not db.session.query(User).filter_by(username="admin").first():
        admin_user = User(
            username="admin",
            password="admin",
            firstname="Admin",
            lastname="User",
            balance=1000.00,
        )
        db.session.add(admin_user)

    
    existing = {s.ticker for s in db.session.query(Security).all()}

    default_securities = [
        ("AAPL", "Apple Inc.", 150.00),
        ("GOOGL", "Alphabet Inc.", 2800.00),
        ("MSFT", "Microsoft Corp.", 300.00),
    ]

    for ticker, issuer, price in default_securities:
        if ticker not in existing:
            db.session.add(Security(ticker=ticker, issuer=issuer, price=price))

    db.session.commit()