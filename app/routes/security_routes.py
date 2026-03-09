from __future__ import annotations

from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

from app.auth.auth import requires_auth
from app.db import db
from app.service import security_service, transaction_service

security_bp = Blueprint("security", __name__)


@security_bp.get("/")
@requires_auth
def get_all_securities():
    try:
        with db.session.no_autoflush:
            securities = security_service.get_all_securities()
        return jsonify(securities), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "detail": str(e)}), 500

@security_bp.get("/<ticker>")
@requires_auth
def get_security(ticker: str):
    try:
        quote = security_service.get_security_by_ticker(ticker)
        if quote is None:
            return jsonify({"error": "Not Found", "detail": f"Security {ticker} not found"}), 404
        return jsonify(quote), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "detail": str(e)}), 500

@security_bp.get("/<ticker>/transactions")
@requires_auth
def get_security_transactions(ticker: str):
    try:
        with db.session.no_autoflush:
            txns = transaction_service.get_transactions_by_ticker(ticker)
        return jsonify([t.__to_dict__() for t in txns]), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "detail": str(e)}), 500