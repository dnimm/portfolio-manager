from __future__ import annotations

from typing import List

from app.db import db
from app.models import Transaction


class TransactionServiceError(Exception):
    pass


def get_transactions_by_user(username: str) -> List[Transaction]:
    if not username:
        raise TransactionServiceError("username cannot be empty")
    try:
        return db.session.query(Transaction).filter(Transaction.username == username).all()
    except Exception as e:
        raise TransactionServiceError(f"Failed to retrieve transactions by user due to error: {str(e)}") from e


def get_transactions_by_portfolio_id(portfolio_id: int) -> List[Transaction]:
    if portfolio_id is None:
        raise TransactionServiceError("portfolio_id cannot be None")
    try:
        return db.session.query(Transaction).filter(Transaction.portfolio_id == portfolio_id).all()
    except Exception as e:
        raise TransactionServiceError(
            f"Failed to retrieve transactions by portfolio due to error: {str(e)}"
        ) from e


def get_transactions_by_ticker(ticker: str) -> List[Transaction]:
    if not ticker:
        raise TransactionServiceError("ticker cannot be empty")
    try:
        return db.session.query(Transaction).filter(Transaction.ticker == ticker).all()
    except Exception as e:
        raise TransactionServiceError(
            f"Failed to retrieve transactions by ticker due to error: {str(e)}"
        ) from e