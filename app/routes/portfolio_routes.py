from __future__ import annotations

from dataclasses import dataclass
from flask import Blueprint, jsonify, request, g

from app.auth.auth import requires_auth
from app.db import db
from app.models import PortfolioAccess
from app.schemas import CreatePortfolioSchema, GrantAccessSchema
from app.service.authorization_service import AuthorizationError, check_portfolio_access
from app.service import portfolio_service, transaction_service, user_service

portfolio_bp = Blueprint("portfolio", __name__)


@dataclass(frozen=True)
class _AuthUser:
    username: str


def _token_username() -> str:
    u = g.current_user or {}
    return (u.get("cognito:username") or u.get("username") or u.get("sub") or "").strip()


@portfolio_bp.get("/")
@requires_auth
def get_all_portfolios():
    portfolios = portfolio_service.get_all_portfolios()
    return jsonify([p.__to_dict__() for p in portfolios]), 200


@portfolio_bp.get("/<int:portfolio_id>")
@requires_auth
def get_portfolio(portfolio_id: int):
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)

    if not portfolio:
        return jsonify({"error": "Not Found", "detail": "Portfolio not found"}), 404

    try:
        check_portfolio_access(_AuthUser(_token_username()), portfolio, "viewer")
    except AuthorizationError as e:
        return jsonify({"error": "Forbidden", "detail": str(e)}), 403

    return jsonify(portfolio.__to_dict__()), 200


@portfolio_bp.get("/user/<username>")
@requires_auth
def get_portfolios_by_user(username: str):
    if username != _token_username():
        return jsonify({"error": "Forbidden", "detail": "Cannot view other users' portfolios"}), 403

    user = user_service.get_user_by_username(username)

    if not user:
        return jsonify({"error": "Not Found", "detail": f"User {username} not found"}), 404

    portfolios = portfolio_service.get_portfolios_by_user(user)
    return jsonify([p.__to_dict__() for p in portfolios]), 200


@portfolio_bp.post("/")
@requires_auth
def create_portfolio():
    payload = CreatePortfolioSchema.model_validate(request.get_json() or {})

    if payload.username != _token_username():
        return jsonify({"error": "Forbidden", "detail": "Cannot create portfolio for another user"}), 403

    user = user_service.get_user_by_username(payload.username)

    if not user:
        return jsonify({"error": "Not Found", "detail": f"User {payload.username} not found"}), 404

    portfolio_id = portfolio_service.create_portfolio(
        payload.name,
        payload.description,
        user,
    )

    db.session.commit()
    return jsonify({"id": portfolio_id}), 201


@portfolio_bp.delete("/<int:portfolio_id>")
@requires_auth
def delete_portfolio(portfolio_id: int):
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)

    if not portfolio:
        return jsonify({"error": "Not Found", "detail": "Portfolio not found"}), 404

    if portfolio.owner != _token_username():
        return jsonify({"error": "Forbidden", "detail": "Only the owner can delete a portfolio"}), 403

    if portfolio.investments:
        return jsonify({
            "error": "Bad Request",
            "detail": "Cannot delete portfolio because it still has holdings"
        }), 400

    portfolio_service.delete_portfolio(portfolio_id)
    db.session.commit()

    return jsonify({"message": "Portfolio deleted successfully"}), 200


@portfolio_bp.get("/<int:portfolio_id>/holdings")
@requires_auth
def get_portfolio_holdings(portfolio_id: int):
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)

    if not portfolio:
        return jsonify({"error": "Not Found", "detail": "Portfolio not found"}), 404

    try:
        check_portfolio_access(_AuthUser(_token_username()), portfolio, "viewer")
    except AuthorizationError as e:
        return jsonify({"error": "Forbidden", "detail": str(e)}), 403

    return jsonify([i.__to_dict__() for i in portfolio.investments]), 200


@portfolio_bp.get("/<int:portfolio_id>/transactions")
@requires_auth
def get_portfolio_transactions(portfolio_id: int):
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)

    if not portfolio:
        return jsonify({"error": "Not Found", "detail": "Portfolio not found"}), 404

    try:
        check_portfolio_access(_AuthUser(_token_username()), portfolio, "viewer")
    except AuthorizationError as e:
        return jsonify({"error": "Forbidden", "detail": str(e)}), 403

    txns = transaction_service.get_transactions_by_portfolio_id(portfolio_id)
    return jsonify([t.__to_dict__() for t in txns]), 200


@portfolio_bp.post("/<int:portfolio_id>/access")
@requires_auth
def grant_access(portfolio_id: int):
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)

    if not portfolio:
        return jsonify({"error": "Not Found", "detail": "Portfolio not found"}), 404

    if portfolio.owner != _token_username():
        return jsonify({"error": "Forbidden", "detail": "Only the owner can grant access"}), 403

    payload = GrantAccessSchema.model_validate(request.get_json() or {})

    target_user = user_service.get_user_by_username(payload.username)

    if not target_user:
        return jsonify({"error": "Not Found", "detail": f"User {payload.username} not found"}), 404

    existing = (
        db.session.query(PortfolioAccess)
        .filter_by(portfolio_id=portfolio_id, username=payload.username)
        .one_or_none()
    )

    if existing:
        existing.role = payload.role
    else:
        db.session.add(
            PortfolioAccess(
                portfolio_id=portfolio_id,
                username=payload.username,
                role=payload.role,
            )
        )

    db.session.commit()
    return jsonify({"message": "Access granted"}), 201


@portfolio_bp.delete("/<int:portfolio_id>/access/<username>")
@requires_auth
def revoke_access(portfolio_id: int, username: str):
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)

    if not portfolio:
        return jsonify({"error": "Not Found", "detail": "Portfolio not found"}), 404

    if portfolio.owner != _token_username():
        return jsonify({"error": "Forbidden", "detail": "Only the owner can revoke access"}), 403

    access = (
        db.session.query(PortfolioAccess)
        .filter_by(portfolio_id=portfolio_id, username=username)
        .one_or_none()
    )

    if not access:
        return jsonify({"error": "Not Found", "detail": "Access grant not found"}), 404

    db.session.delete(access)
    db.session.commit()

    return jsonify({"message": "Access revoked"}), 200