from portfolioapp.db import db
from portfolioapp.domain.transaction import Transaction

def record_transaction(pid, ticker, txn_type, qty, price):
    t = Transaction(
        portfolio_id=pid,
        ticker=ticker,
        txn_type=txn_type,
        quantity=qty,
        price=price
    )
    db.session.add(t)
    db.session.commit()

def get_transactions():
    return Transaction.query.all()
