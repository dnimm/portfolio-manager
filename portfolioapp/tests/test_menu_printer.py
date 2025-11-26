import pytest
from portfolioapp.cli import menu_printer
from portfolioapp.cli import constants
from portfolioapp.database import get_session
from portfolioapp.domain.transaction import Transaction
from datetime import datetime



def test_menu_printer_imports():
    assert menu_printer is not None




def test_view_transactions_empty(monkeypatch):
    
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: None)

    
    monkeypatch.setattr(menu_printer, "_console", type("X", (), {"print": lambda *a, **k: None})())

    try:
        menu_printer.view_transactions()
    except Exception:
        assert False, "view_transactions() on empty DB should not crash"



def test_view_transactions_with_record(monkeypatch, db_session):
    
    t = Transaction(
        portfolio_id=1,
        ticker="AAPL",
        txn_type="BUY",
        quantity=5,
        price=150.0,
        timestamp=datetime.now()
    )
    db_session.add(t)
    db_session.commit()

    
    monkeypatch.setattr(menu_printer, "_console", type("X", (), {"print": lambda *a, **k: None})())

    try:
        menu_printer.view_transactions()
    except Exception:
        assert False, "view_transactions() with a record should not crash"
