from __future__ import annotations

import base64
import os
from urllib.parse import urlencode

import requests
from flask import Blueprint, jsonify, request, redirect
from jose import jwt
from sqlalchemy.exc import IntegrityError

from app.auth.auth import requires_auth
from app.db import db
from app.models import User
from app.service import transaction_service, user_service

user_bp = Blueprint("user", __name__)


@user_bp.get("/login")
def cognito_login():
    domain = os.environ.get("COGNITO_DOMAIN")
    client_id = os.environ.get("COGNITO_CLIENT_ID")
    redirect_uri = os.environ.get("COGNITO_REDIRECT_URI")

    params = {
        "client_id": client_id,
        "response_type": "code",
        "scope": "openid email",
        "redirect_uri": redirect_uri,
    }

    return redirect(f"{domain}/oauth2/authorize?{urlencode(params)}")


def create_user_if_missing(access_token: str):
    claims = jwt.get_unverified_claims(access_token)

    username = (
        claims.get("username")
        or claims.get("cognito:username")
        or claims.get("sub")
    )

    email = claims.get("email", "")

    if not username:
        return

    existing_user = db.session.query(User).filter_by(username=username).one_or_none()

    if existing_user:
        return

    new_user = User(
        username=username,
        password="cognito",
        firstname=email.split("@")[0] if email else "Cognito",
        lastname="User",
        balance=10000.00,
    )

    db.session.add(new_user)
    db.session.commit()


@user_bp.get("/callback")
def cognito_callback():
    code = request.args.get("code")
    error = request.args.get("error")
    error_description = request.args.get("error_description")

    if error:
        return jsonify({
            "error": error,
            "detail": error_description,
            "received_args": request.args.to_dict(),
        }), 400

    if not code:
        return jsonify({
            "error": "Missing authorization code",
            "received_args": request.args.to_dict(),
        }), 400

    domain = os.environ.get("COGNITO_DOMAIN")
    client_id = os.environ.get("COGNITO_CLIENT_ID")
    client_secret = os.environ.get("COGNITO_CLIENT_SECRET")
    redirect_uri = os.environ.get("COGNITO_REDIRECT_URI")
    frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:5173")

    basic_token = base64.b64encode(
        f"{client_id}:{client_secret}".encode("utf-8")
    ).decode("utf-8")

    response = requests.post(
        f"{domain}/oauth2/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {basic_token}",
        },
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "code": code,
            "redirect_uri": redirect_uri,
        },
        timeout=10,
    )

    data = response.json()

    if response.status_code != 200:
        return jsonify(data), response.status_code

    access_token = data.get("access_token", "")

    create_user_if_missing(access_token)

    return redirect(f"{frontend_url}?token={access_token}")


@user_bp.get("/<username>")
@requires_auth
def get_user(username: str):
    try:
        user = user_service.get_user_by_username(username)

        if user is None:
            return jsonify({
                "error": "Not Found",
                "detail": f"User {username} not found"
            }), 404

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
        return jsonify({
            "error": "Bad Request",
            "detail": f"Duplicate/invalid user: {str(e)}"
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error", "detail": str(e)}), 500


@user_bp.put("/update-balance")
@requires_auth
def update_balance():
    try:
        req = request.get_json() or {}

        user_service.update_user_balance(
            username=req.get("username"),
            new_balance=req.get("new_balance"),
        )

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