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


def test_action_list_requires_authenticated_tenant_context() -> None:
    email = f"actions-{uuid.uuid4()}@example.com"
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Action Lab"},
    )
    assert register_response.status_code == 201
    token = register_response.json()["tokens"]["access_token"]

    response = client.get(
        "/api/v1/actions",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["organization_name"] == "Action Lab"
    assert payload["actions"][0]["priority"] in {"High", "Medium"}


def test_action_list_uses_customer_risk_signals() -> None:
    email = f"risk-actions-{uuid.uuid4()}@example.com"
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Intervention Lab"},
    )
    assert register_response.status_code == 201
    token = register_response.json()["tokens"]["access_token"]

    import_response = client.post(
        "/api/v1/customers/import",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "csv": "name,email,company,status,health_score,monthly_revenue,segment\nJane Doe,jane@example.com,Northwind,At risk,44,12500,SMB\nMia Chen,mia@example.com,Harbor,Critical,18,9000,SMB\n"
        },
    )
    assert import_response.status_code == 200

    response = client.get(
        "/api/v1/actions",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["organization_name"] == "Intervention Lab"
    titles = [item["title"] for item in payload["actions"]]
    assert any("Mia" in title or "Critical" in title for title in titles)
    assert any("Jane" in title or "At risk" in title for title in titles)


def test_customer_import_creates_tenant_scoped_records() -> None:
    email = f"import-{uuid.uuid4()}@example.com"
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Import Lab"},
    )
    assert register_response.status_code == 201
    token = register_response.json()["tokens"]["access_token"]

    csv_payload = "name,email,company,status,health_score,monthly_revenue,segment\nJane Doe,jane@example.com,Northwind,At risk,44,12500,SMB\nOmar Ali,omar@example.com,Blue Harbor,Healthy,86,21000,Growth\n"
    import_response = client.post(
        "/api/v1/customers/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"csv": csv_payload},
    )

    assert import_response.status_code == 200
    imported = import_response.json()
    assert imported["created"] >= 2
    assert imported["organization_name"] == "Import Lab"

    list_response = client.get(
        "/api/v1/customers",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_response.status_code == 200
    customers = list_response.json()["customers"]
    assert any(customer["email"] == "jane@example.com" for customer in customers)
    assert any(customer["email"] == "omar@example.com" for customer in customers)
