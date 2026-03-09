from app.auth import auth


def test_protected_route_no_token_returns_403(client):
    resp = client.get("/portfolios/")
    assert resp.status_code == 403


def test_protected_route_invalid_token_returns_403(monkeypatch, client):
    def fake_validate(_token):
        raise ValueError("Invalid token")

    monkeypatch.setattr(auth, "validate_token", fake_validate)

    resp = client.get("/portfolios/", headers={"Authorization": "Bearer badtoken"})
    assert resp.status_code == 403


def test_protected_route_valid_token_allows_access(monkeypatch, client):
    def fake_validate(_token):
        return {"sub": "abc", "token_use": "access"}

    monkeypatch.setattr(auth, "validate_token", fake_validate)

    resp = client.get("/portfolios/", headers={"Authorization": "Bearer goodtoken"})
    assert resp.status_code != 403