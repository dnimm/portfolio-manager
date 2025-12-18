from flask import Blueprint, request, jsonify
from portfolioapp.services.portfolio_service import *

portfolio_bp = Blueprint("portfolios", __name__, url_prefix="/portfolios/")

@portfolio_bp.get("")
def all_ports():
    return jsonify([p.name for p in get_all_portfolios()])

@portfolio_bp.post("")
def create():
    p = create_portfolio(request.json)
    return jsonify({"id": p.id})

@portfolio_bp.post("/<int:pid>/buy")
def buy(pid):
    ok = buy_security(pid, request.json)
    return jsonify({"status": "ok"}) if ok else jsonify({"error": "insufficient"}), 400
