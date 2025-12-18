from flask import Blueprint, jsonify
from portfolioapp.services.transaction_service import get_transactions

transaction_bp = Blueprint("transactions", __name__, url_prefix="/transactions/")

@transaction_bp.get("")
def all_tx():
    return jsonify([
        {
            "ticker": t.ticker,
            "type": t.txn_type,
            "qty": t.quantity,
            "price": t.price
        }
        for t in get_transactions()
    ])
