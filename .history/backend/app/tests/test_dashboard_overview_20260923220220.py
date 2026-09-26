import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_overview_requires_authenticated_tenant_context() -> None:
    email = f"dashboard-{uuid.uuid4()}@example.com"
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Northwind Labs"},
    )
    assert register_response.status_code == 201
    token = register_response.json()["tokens"]["access_token"]

    response = client.get(
        "/api/v1/dashboard/overview",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["organization"]["name"] == "Northwind Labs"
    assert payload["snapshot"]["total_customers"] >= 0
    assert payload["snapshot"]["at_risk_customers"] >= 0


def test_dashboard_overview_uses_customer_health_signals() -> None:
    email = f"dashboard-risk-{uuid.uuid4()}@example.com"
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Risk Labs"},
    )
    assert register_response.status_code == 201
    token = register_response.json()["tokens"]["access_token"]

    import_response = client.post(
        "/api/v1/customers/import",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "csv": "name,email,company,status,health_score,monthly_revenue,segment\nJane Doe,jane@example.com,Northwind,At risk,44,12500,SMB\nOmar Ali,omar@example.com,Blue Harbor,Healthy,86,21000,Growth\nMia Chen,mia@example.com,Harbor,Critical,18,9000,SMB\n"
        },
    )
    assert import_response.status_code == 200

    response = client.get(
        "/api/v1/dashboard/overview",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["organization"]["name"] == "Risk Labs"
    assert payload["snapshot"]["total_customers"] == 3
    assert payload["snapshot"]["critical_customers"] >= 1
    assert payload["snapshot"]["at_risk_customers"] >= 1
