from __future__ import annotations

import datetime

from app.db import db
from app.models import Investment, Portfolio, Security, Transaction
from app.service.alpha_vantage_client import get_quote


class TradeExecutionException(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


def buy_trade(portfolio_id: int, ticker: str, quantity: int) -> None:
    
    if portfolio_id is None or not ticker or quantity is None or quantity <= 0:
        raise TradeExecutionException(
            f"Invalid buy order parameters [portfolio_id={portfolio_id}, ticker={ticker}, quantity={quantity}]"
        )

    ticker = ticker.upper().strip()

    portfolio = db.session.query(Portfolio).filter_by(id=portfolio_id).one_or_none()
    if not portfolio:
        raise TradeExecutionException(f"Portfolio with id {portfolio_id} does not exist.")

    user = portfolio.user
    if not user:
        raise TradeExecutionException(f"User associated with portfolio {portfolio_id} does not exist.")

    quote = get_quote(ticker)
    if not quote:
        raise TradeExecutionException(f"Security with ticker {ticker} could not be resolved.")

    price = float(quote.price)
    total_cost = price * quantity

    if user.balance < total_cost:
        raise InsufficientFundsError("Insufficient funds to complete the purchase.")

    security = db.session.query(Security).filter_by(ticker=quote.ticker).first()

    if security:
        security.issuer = quote.issuer
        security.price = price
    else:
        security = Security(
            ticker=quote.ticker,
            issuer=quote.issuer,
            price=price
    )
        db.session.add(security)

    existing_investment = next((inv for inv in portfolio.investments if inv.ticker == quote.ticker), None)
    if existing_investment:
        existing_investment.quantity += quantity
    else:
        portfolio.investments.append(Investment(ticker=quote.ticker, quantity=quantity, security=security))

    user.balance -= total_cost

    db.session.add(
        Transaction(
            portfolio_id=portfolio.id,
            username=user.username,
            ticker=quote.ticker,
            quantity=quantity,
            price=price,
            transaction_type="BUY",
            date_time=datetime.datetime.now(),
        )
    )


def sell_trade(portfolio_id: int, ticker: str, quantity: int) -> None:
   
    if portfolio_id is None or not ticker or quantity is None or quantity <= 0:
        raise TradeExecutionException(
            f"Invalid sell order parameters [portfolio_id={portfolio_id}, ticker={ticker}, quantity={quantity}]"
        )

    ticker = ticker.upper().strip()

    portfolio = db.session.query(Portfolio).filter_by(id=portfolio_id).one_or_none()
    if not portfolio:
        raise TradeExecutionException(f"Portfolio with id {portfolio_id} does not exist.")

    user = portfolio.user
    if not user:
        raise TradeExecutionException(f"User associated with portfolio {portfolio_id} does not exist.")

    investment = next((inv for inv in portfolio.investments if inv.ticker == ticker), None)
    if not investment:
        raise TradeExecutionException(f"No investment with ticker {ticker} exists in portfolio with id {portfolio_id}")

    if investment.quantity < quantity:
        raise TradeExecutionException(
            f"Cannot liquidate {quantity} shares of {ticker}. Only {investment.quantity} shares available in portfolio"
        )

    quote = get_quote(ticker)
    if not quote:
        raise TradeExecutionException(f"Security with ticker {ticker} could not be resolved.")

    sale_price = float(quote.price)
    total_proceeds = sale_price * quantity

    user.balance += total_proceeds

    if investment.quantity == quantity:
        if investment in portfolio.investments:
            portfolio.investments.remove(investment)
        db.session.delete(investment)
    else:
        investment.quantity -= quantity

    db.session.add(
        Transaction(
            portfolio_id=portfolio.id,
            username=user.username,
            ticker=quote.ticker,
            quantity=quantity,
            price=sale_price,
            transaction_type="SELL",
            date_time=datetime.datetime.now(),
        )
    )
