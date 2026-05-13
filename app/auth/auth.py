from __future__ import annotations

import functools
from typing import Optional

import requests
from flask import current_app, g, jsonify, request, Blueprint
from jose import JWTError, jwt
import base64
import os
from urllib.parse import urlencode

import requests

_jwks_cache: Optional[dict] = None


def _jwks_url() -> str:
    region = current_app.config.get("COGNITO_REGION", "")
    pool_id = current_app.config.get("COGNITO_POOL_ID", "")
    return f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"


def _issuer() -> str:
    region = current_app.config.get("COGNITO_REGION", "")
    pool_id = current_app.config.get("COGNITO_POOL_ID", "")
    return f"https://cognito-idp.{region}.amazonaws.com/{pool_id}"


def _get_jwks() -> dict:
    global _jwks_cache
    if _jwks_cache:
        return _jwks_cache

    resp = requests.get(_jwks_url(), timeout=10)
    resp.raise_for_status()
    data = resp.json() or {}

    keys = {}
    for k in data.get("keys", []):
        kid = k.get("kid")
        if kid:
            keys[kid] = k

    _jwks_cache = keys
    return _jwks_cache


def validate_token(token: str) -> dict:
    client_id = current_app.config.get("COGNITO_CLIENT_ID", "")

    header = jwt.get_unverified_header(token)
    kid = header.get("kid")

    jwks = _get_jwks()
    key = jwks.get(kid)

    claims = jwt.decode(
        token,
        key,
        algorithms=["RS256"],
        audience=client_id,
        issuer=_issuer(),
    )

    if claims.get("token_use") != "access":
        raise ValueError("Token is not an access token")

    return claims


def requires_auth(handler):
    @functools.wraps(handler)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Forbidden", "detail": "Missing or invalid Authorization header"}), 403

        token = auth_header.split(" ", 1)[1].strip()

        try:
            claims = validate_token(token)
        except Exception as e:
            return jsonify({"error": "Forbidden", "detail": str(e)}), 403

        g.current_user = claims
        return handler(*args, **kwargs)

    return wrapper