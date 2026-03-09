from typing import List

import app.database as database
from app.models import Portfolio, User


class UnsupportedPortfolioOperationError(Exception):
    pass


class PortfolioOperationError(Exception):
    pass


def create_portfolio(name: str, description: str, user: User) -> int:
    if not name or not description or not user:
        raise UnsupportedPortfolioOperationError(
            f"Invalid input[name:{name}, description:{description}, user:{user}]. Please try again."
        )

    try:
        session = database.get_session()
        portfolio = Portfolio(name=name, description=description, user=user)
        session.add(portfolio)
        session.flush()
        return portfolio.id
    except Exception as e:
        raise PortfolioOperationError(
            f"Failed to create portfolio due to error: {str(e)}"
        )


def get_all_portfolios() -> List[Portfolio]:
    try:
        session = database.get_session()
        return session.query(Portfolio).all()
    except Exception as e:
        raise PortfolioOperationError(
            f"Failed to retrieve portfolios due to error: {str(e)}"
        )


def get_portfolios_by_user(user: User) -> List[Portfolio]:
    try:
        session = database.get_session()
        return session.query(Portfolio).filter_by(owner=user.username).all()
    except Exception as e:
        raise PortfolioOperationError(
            f"Failed to retrieve portfolios due to error: {str(e)}"
        )


def get_portfolio_by_id(portfolio_id: int) -> Portfolio | None:
    try:
        session = database.get_session()
        return session.query(Portfolio).filter_by(id=portfolio_id).one_or_none()
    except Exception as e:
        raise PortfolioOperationError(
            f"Failed to retrieve portfolio due to error: {str(e)}"
        )


def delete_portfolio(portfolio_id: int):
    session = database.get_session()
    portfolio = session.query(Portfolio).filter_by(id=portfolio_id).one_or_none()
    if not portfolio:
        raise UnsupportedPortfolioOperationError(
            f"Portfolio with id {portfolio_id} does not exist"
        )
    session.delete(portfolio)
    session.flush()