import pytest
from flask import Flask

from app import create_app
from app.config import TestConfig
from app.service.authorization_service import AuthorizationError


def test_authorization_error_handler_rolls_back(app, client):
    
    @app.get("/raise-authz")
    def raise_authz():
        raise AuthorizationError("no")

    resp = client.get("/raise-authz")
    assert resp.status_code == 403
    body = resp.get_json()
    assert body["error"] == "Forbidden"


def test_generic_error_handler(app, client):
    @app.get("/b")
    def b():
        raise RuntimeError("b")

    resp = client.get("/b")
    assert resp.status_code == 500
    body = resp.get_json()
    assert body["error"] == "Internal Server Error"