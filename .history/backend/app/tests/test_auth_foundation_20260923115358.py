import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_endpoint_creates_user_and_tokens() -> None:
    email = f"register-{uuid.uuid4()}@example.com"
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Acme"},
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["user"]["email"] == email
    assert payload["organization"]["name"] == "Acme"
    assert payload["tokens"]["token_type"] == "bearer"
    assert payload["tokens"]["access_token"]


def test_login_endpoint_authenticates_user() -> None:
    email = f"login-{uuid.uuid4()}@example.com"
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Acme"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Password123!"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["user"]["email"] == email
    assert payload["tokens"]["access_token"]


def test_login_with_invalid_password_returns_401() -> None:
    email = f"invalid-{uuid.uuid4()}@example.com"
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Acme"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "WrongPassword!"},
    )
    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["code"] == "AUTHENTICATION_ERROR"
