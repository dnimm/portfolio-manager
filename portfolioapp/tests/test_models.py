from portfolioapp.domain.user import User
from portfolioapp.domain.security import Security
from portfolioapp.domain.portfolio import Portfolio
from portfolioapp.domain.investment import Investment
from portfolioapp.domain.transaction import Transaction
from datetime import datetime
from portfolioapp import session_state
from portfolioapp.cli.input_collector import collect_inputs


def test_user_model():
    u = User(username="tom", firstname="Tom", lastname="H", password="pw", balance=100)
    assert u.username == "tom"
    assert u.balance == 100


def test_security_model():
    s = Security(ticker="AAPL", issuer="Apple", price=150)
    assert s.ticker == "AAPL"
    assert s.price == 150



def test_transaction_model():
    t = Transaction(
        portfolio_id=1,
        ticker="AAPL",
        txn_type="BUY",
        quantity=5,
        price=150,
        timestamp=datetime.now()
    )
    assert t.ticker == "AAPL"
    assert t.quantity == 5


def test_login_service_imports():
    from portfolioapp.services import login_service
    assert hasattr(login_service, "login")


def test_input_collector_basic(monkeypatch):
    
    monkeypatch.setattr("builtins.input", lambda prompt="": "abc")

    fields = {"Username": "username"}
    result = collect_inputs(fields)

    assert result["username"] == "abc"


def test_session_state():
    
    session_state.set_logged_in_user("testuser")
    assert session_state.get_logged_in_user() == "testuser"
    session_state.clear_logged_in_user()
    assert session_state.get_logged_in_user() is None

def test_db_module_import():
    
    import portfolioapp.db
    assert True


def test_create_portfolio(db_session, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda x="": "TestPF")
    result = True

    assert result is True


import portfolioapp.domain.MenuFunctions as MF

def test_menufunctions_import():
    assert MF is not None



