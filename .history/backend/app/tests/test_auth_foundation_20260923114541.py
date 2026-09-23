from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_endpoint_is_placeholder() -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "Password123!", "organization_name": "Acme"},
    )
    assert response.status_code == 501
    payload = response.json()
    assert payload["error"]["code"] == "NOT_IMPLEMENTED"


def test_login_endpoint_is_placeholder() -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "Password123!"},
    )
    assert response.status_code == 501
    payload = response.json()
    assert payload["error"]["code"] == "NOT_IMPLEMENTED"
