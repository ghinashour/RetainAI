import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_customer_list_requires_authenticated_tenant_context() -> None:
    email = f"customers-{uuid.uuid4()}@example.com"
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Northwind Labs"},
    )
    assert register_response.status_code == 201
    token = register_response.json()["tokens"]["access_token"]

    response = client.get(
        "/api/v1/customers",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["organization_name"] == "Northwind Labs"
    assert len(payload["customers"]) >= 1
    assert payload["customers"][0]["status"] in {"At risk", "Healthy", "Critical"}
