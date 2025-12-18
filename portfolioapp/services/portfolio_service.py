from portfolioapp.db import db
from portfolioapp.domain.portfolio import Portfolio
from portfolioapp.domain.security import Security
from portfolioapp.domain.investment import Investment
from portfolioapp.services.transaction_service import record_transaction

def get_all_portfolios():
    return Portfolio.query.all()

def create_portfolio(data):
    p = Portfolio(**data)
    db.session.add(p)
    db.session.commit()
    return p

def buy_security(pid, data):
    p = Portfolio.query.get(pid)
    sec = Security.query.filter_by(ticker=data["ticker"]).first()

    cost = sec.price * data["quantity"]
    if p.user.balance < cost:
        return False

    p.user.balance -= cost

    inv = Investment(
        portfolio_id=pid,
        ticker=sec.ticker,
        quantity=data["quantity"],
        purchase_price=sec.price
    )
    db.session.add(inv)
    db.session.commit()
    record_transaction(pid, sec.ticker, "BUY", data["quantity"], sec.price)
    return True
