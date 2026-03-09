from __future__ import annotations

from typing import List, Optional

from app.db import db
from app.models import Security
from app.service.alpha_vantage_client import get_quote
from app.service import trade_service


class SecurityException(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


def get_all_securities() -> List[dict]:
    
    rows = db.session.query(Security).all()
    return [s.__to_dict__() for s in rows]


def get_security_by_ticker(ticker: str) -> Optional[dict]:
    
    q = get_quote(ticker)
    if not q:
        return None

    return {
        "ticker": q.ticker,
        "issuer": q.issuer,
        "price": q.price,
        "date": q.date,
    }


def execute_purchase_order(portfolio_id: int, ticker: str, quantity: int) -> None:
  
    try:
        trade_service.buy_trade(portfolio_id, ticker, quantity)
    except trade_service.InsufficientFundsError as e:
        
        raise InsufficientFundsError(str(e)) from e
    except Exception as e:
        raise SecurityException(str(e)) from e