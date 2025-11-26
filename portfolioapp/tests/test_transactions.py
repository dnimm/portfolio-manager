from portfolioapp.services.transaction_service import record_transaction
from portfolioapp.domain.transaction import Transaction
import portfolioapp.database as database
import pytest


def test_record_transaction(db_session):
    
    record_transaction(
        portfolio_id=1,
        ticker="AAPL",
        txn_type="BUY",
        qty=5,
        price=150.0
    ) 
    t = db_session.query(Transaction).filter_by(ticker="AAPL").first()

    assert t is not None
    assert t.txn_type == "BUY"
    assert t.quantity == 5
    assert t.price == 150
    
def test_multiple_transactions(db_session):
    record_transaction(1, "AMZN", "BUY", 2, 100.0)
    record_transaction(1, "AMZN", "SELL", 1, 120.0)

    txns = db_session.query(Transaction).filter_by(ticker="AMZN").all()
    assert len(txns) == 2