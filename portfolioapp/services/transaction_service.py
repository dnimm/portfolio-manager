from portfolioapp.database import get_session
from portfolioapp.domain.transaction import Transaction
import portfolioapp.database as database
import pytest

def record_transaction(portfolio_id: int, ticker: str, txn_type: str, qty: int, price: float):
    try:
        session = database.get_session()
        t = Transaction(
            portfolio_id=portfolio_id,
            ticker=ticker,
            txn_type=txn_type,
            quantity=qty,
            price=price
        )
        session.add(t)
        session.commit()
    except Exception as e:
        print(f"Transaction error: {str(e)}")
    finally:
        session.close() if 'session' in locals() else None
    

