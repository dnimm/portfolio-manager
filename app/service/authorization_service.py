from __future__ import annotations

from typing import Any

from app.db import db
from app.models import Portfolio, PortfolioAccess


class AuthorizationError(Exception):
    pass


def _get_username(user: Any) -> str:
   
    if isinstance(user, dict):
        return (
            user.get("username")
            or user.get("cognito:username")
            or user.get("sub")
            or ""
        )
    return getattr(user, "username", "")


def check_portfolio_access(user: Any, portfolio: Portfolio, required_role: str) -> bool:
   
    username = _get_username(user)
    if not username:
        raise AuthorizationError("Missing user identity")

    
    if portfolio.owner == username:
        return True

    access = (
        db.session.query(PortfolioAccess)
        .filter_by(portfolio_id=portfolio.id, username=username)
        .one_or_none()
    )

    if not access:
        raise AuthorizationError("User has no access to this portfolio")

    if required_role == "viewer":
        return True

    if required_role == "manager" and access.role == "manager":
        return True

    raise AuthorizationError("Insufficient permissions")