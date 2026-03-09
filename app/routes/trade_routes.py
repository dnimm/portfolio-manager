from __future__ import annotations

from dataclasses import dataclass

from flask import Blueprint, jsonify, request, g

from app.auth.auth import requires_auth
from app.db import db
from app.schemas import BuyTradeSchema, SellTradeSchema
from app.service.authorization_service import AuthorizationError, check_portfolio_access
from app.service import portfolio_service, trade_service

trade_bp = Blueprint("trade", __name__)


@dataclass(frozen=True)
class _AuthUser:
    username: str


def _token_username() -> str:
    u = g.current_user or {}
    return (u.get("username") or u.get("cognito:username") or u.get("sub") or "").strip()


@trade_bp.post("/buy")
@requires_auth
def buy():
    payload = BuyTradeSchema.model_validate(request.get_json() or {})

    portfolio = portfolio_service.get_portfolio_by_id(payload.portfolio_id)
    if not portfolio:
        return jsonify({"error": "Not Found", "detail": "Portfolio not found"}), 404

    try:
        check_portfolio_access(_AuthUser(_token_username()), portfolio, "manager")
    except AuthorizationError as e:
        return jsonify({"error": "Forbidden", "detail": str(e)}), 403

    trade_service.buy_trade(payload.portfolio_id, payload.ticker, payload.quantity)
    db.session.commit()
    return jsonify({"message": "buy order executed"}), 201


@trade_bp.post("/sell")
@requires_auth
def sell():
    payload = SellTradeSchema.model_validate(request.get_json() or {})

    portfolio = portfolio_service.get_portfolio_by_id(payload.portfolio_id)
    if not portfolio:
        return jsonify({"error": "Not Found", "detail": "Portfolio not found"}), 404

    try:
        check_portfolio_access(_AuthUser(_token_username()), portfolio, "manager")
    except AuthorizationError as e:
        return jsonify({"error": "Forbidden", "detail": str(e)}), 403

    trade_service.sell_trade(payload.portfolio_id, payload.ticker, payload.quantity)
    db.session.commit()
    return jsonify({"message": "sell order executed"}), 201