from __future__ import annotations

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from app.auth.auth import requires_auth
from app.db import db
from app.service import transaction_service, user_service

user_bp = Blueprint("user", __name__)


@user_bp.get("/")
@requires_auth
def get_users():
    
        users = user_service.get_all_users()
        return jsonify([u.__to_dict__() for u in users]), 200
    


@user_bp.get("/<username>")
@requires_auth
def get_user(username: str):
    try:
        user = user_service.get_user_by_username(username)
        if user is None:
            return jsonify({"error": "Not Found", "detail": f"User {username} not found"}), 404
        return jsonify(user.__to_dict__()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "detail": str(e)}), 500


@user_bp.post("/")
@requires_auth
def create_user():
    try:
        req = request.get_json() or {}

        user_service.create_user(
            username=req.get("username"),
            password=req.get("password"),
            firstname=req.get("firstname"),
            lastname=req.get("lastname"),
            balance=req.get("balance"),
        )

        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Bad Request", "detail": f"Duplicate/invalid user: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "detail": str(e)}), 500


@user_bp.put("/update-balance")
@requires_auth
def update_balance():
    try:
        req = request.get_json() or {}
        user_service.update_user_balance(username=req.get("username"), new_balance=req.get("new_balance"))
        db.session.commit()
        return jsonify({"message": "User balance updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "detail": str(e)}), 500


@user_bp.delete("/<username>")
@requires_auth
def delete_user(username: str):
    try:
        user_service.delete_user(username)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "detail": str(e)}), 500


@user_bp.get("/<username>/transactions")
@requires_auth
def get_user_transactions(username: str):
    try:
        with db.session.no_autoflush:
            txns = transaction_service.get_transactions_by_user(username)
        return jsonify([t.__to_dict__() for t in txns]), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "detail": str(e)}), 500