from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_endpoint_creates_user_and_tokens() -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "Password123!", "organization_name": "Acme"},
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["user"]["email"] == "test@example.com"
    assert payload["organization"]["name"] == "Acme"
    assert payload["tokens"]["token_type"] == "bearer"
    assert payload["tokens"]["access_token"]


def test_login_endpoint_authenticates_user() -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "Password123!"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["user"]["email"] == "test@example.com"
    assert payload["tokens"]["access_token"]


def test_login_with_invalid_password_returns_401() -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "WrongPassword!"},
    )
    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["code"] == "AUTHENTICATION_ERROR"
