from flask import Blueprint, request, jsonify
from portfolioapp.services.security_service import *

security_bp = Blueprint("securities", __name__, url_prefix="/securities/")

@security_bp.get("")
def all_secs():
    return jsonify([s.ticker for s in get_all_securities()])

@security_bp.post("")
def create():
    create_security(request.json)
    return jsonify({"status": "created"})
