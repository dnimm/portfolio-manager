import json
from flask import g
from app.auth import auth


def test_jwks_helpers(app, monkeypatch):
    with app.app_context():
        
        app.config["COGNITO_REGION"] = "us-east-1"
        app.config["COGNITO_POOL_ID"] = "pool123"
        app.config["COGNITO_CLIENT_ID"] = "client123"

        assert "us-east-1" in auth._jwks_url()
        assert "pool123" in auth._jwks_url()
        assert "us-east-1" in auth._issuer()


def test_validate_token_success_branch(app, monkeypatch):
    with app.app_context():
        app.config["COGNITO_CLIENT_ID"] = "client123"

        # fake jwks
        monkeypatch.setattr(auth, "_get_jwks", lambda: {"k1": {"kty": "RSA"}})

        monkeypatch.setattr(auth.jwt, "get_unverified_header", lambda t: {"k": "k1"})

        monkeypatch.setattr(
            auth.jwt,
            "decode",
            lambda *args, **kwargs: {"token_use": "access", "username": "x"},
        )

        claims = auth.validate_token("d")
        assert claims["username"] == "x"

