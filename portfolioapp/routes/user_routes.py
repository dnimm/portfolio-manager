from flask import Blueprint, request, jsonify
from portfolioapp.services.user_service import *

user_bp = Blueprint("users", __name__, url_prefix="/users/")

@user_bp.get("")
def all_users():
    return jsonify([u.username for u in get_all_users()])

@user_bp.post("")
def create():
    u = create_user(request.json)
    return jsonify({"status": "created"}) if u else jsonify({"error": "exists"}), 400
