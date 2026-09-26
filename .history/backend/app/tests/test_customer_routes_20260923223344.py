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


def test_intervention_and_outcome_tracking_is_tenant_scoped() -> None:
    email = f"intervention-{uuid.uuid4()}@example.com"
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Intervention Studio"},
    )
    assert register_response.status_code == 201
    token = register_response.json()["tokens"]["access_token"]

    import_response = client.post(
        "/api/v1/customers/import",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "csv": "name,email,company,status,health_score,monthly_revenue,segment\nDrew Hall,drew@example.com,Northwind,Critical,29,15000,Enterprise\n"
        },
    )
    assert import_response.status_code == 200
    customer_id = client.get("/api/v1/customers", headers={"Authorization": f"Bearer {token}"}).json()["customers"][0]["id"]

    intervention_response = client.post(
        "/api/v1/interventions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "customer_id": customer_id,
            "title": "Renewal recovery call",
            "channel": "email",
            "status": "scheduled",
            "notes": "Follow up with expansion proposal and usage review",
        },
    )
    assert intervention_response.status_code == 200
    created = intervention_response.json()
    assert created["organization_name"] == "Intervention Studio"
    assert created["intervention"]["title"] == "Renewal recovery call"

    outcome_response = client.post(
        "/api/v1/outcomes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "customer_id": customer_id,
            "status": "positive",
            "value": 2400,
            "note": "Customer renewed after outreach",
        },
    )
    assert outcome_response.status_code == 200
    outcome = outcome_response.json()
    assert outcome["organization_name"] == "Intervention Studio"
    assert outcome["outcome"]["status"] == "positive"

    list_response = client.get("/api/v1/interventions", headers={"Authorization": f"Bearer {token}"})
    assert list_response.status_code == 200
    interventions = list_response.json()["interventions"]
    assert len(interventions) >= 1

    outcomes_response = client.get("/api/v1/outcomes", headers={"Authorization": f"Bearer {token}"})
    assert outcomes_response.status_code == 200
    outcomes = outcomes_response.json()["outcomes"]
    assert len(outcomes) >= 1


def test_recommendations_and_analytics_are_tenant_scoped() -> None:
    email = f"analytics-{uuid.uuid4()}@example.com"
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Insight Lab"},
    )
    assert register_response.status_code == 201
    token = register_response.json()["tokens"]["access_token"]

    customer_payload = (
        "name,email,company,status,health_score,monthly_revenue,segment\n"
        "Alicia Park,alicia@example.com,Northwind,At risk,52,18000,Enterprise\n"
        "Milo Chen,milo@example.com,Harbor,Critical,28,9000,SMB\n"
    )
    import_response = client.post(
        "/api/v1/customers/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"csv": customer_payload},
    )
    assert import_response.status_code == 200

    customer_id = client.get("/api/v1/customers", headers={"Authorization": f"Bearer {token}"}).json()["customers"][0]["id"]
    intervention_response = client.post(
        "/api/v1/interventions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "customer_id": customer_id,
            "title": "Expansion recovery plan",
            "channel": "email",
            "status": "scheduled",
            "notes": "Deliver renewal offer and usage review",
        },
    )
    assert intervention_response.status_code == 200

    outcome_response = client.post(
        "/api/v1/outcomes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "customer_id": customer_id,
            "status": "positive",
            "value": 4200,
            "note": "Customer accepted expansion after outreach",
        },
    )
    assert outcome_response.status_code == 200

    recommendations_response = client.get("/api/v1/recommendations", headers={"Authorization": f"Bearer {token}"})
    assert recommendations_response.status_code == 200
    recommendations = recommendations_response.json()["recommendations"]
    assert len(recommendations) >= 1
    assert any("renewal" in item["title"].lower() or "expansion" in item["title"].lower() for item in recommendations)

    analytics_response = client.get("/api/v1/analytics/summary", headers={"Authorization": f"Bearer {token}"})
    assert analytics_response.status_code == 200
    analytics = analytics_response.json()
    assert analytics["organization_name"] == "Insight Lab"
    assert analytics["summary"]["total_customers"] >= 2
    assert analytics["summary"]["positive_outcomes"] >= 1


def test_assistant_briefing_uses_live_retention_data() -> None:
    email = f"assistant-{uuid.uuid4()}@example.com"
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "organization_name": "Northwind Retention"},
    )
    assert register_response.status_code == 201
    token = register_response.json()["tokens"]["access_token"]

    import_response = client.post(
        "/api/v1/customers/import",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "csv": "name,email,company,status,health_score,monthly_revenue,segment\n"
            "Rhea Smith,rhea@example.com,Atlas,At risk,46,16000,Enterprise\n"
            "Leo Park,leo@example.com,Harbor,Critical,22,7000,SMB\n"
        },
    )
    assert import_response.status_code == 200

    briefing_response = client.get("/api/v1/assistant/briefing", headers={"Authorization": f"Bearer {token}"})
    assert briefing_response.status_code == 200
    briefing = briefing_response.json()
    assert briefing["organization_name"] == "Northwind Retention"
    assert briefing["headline"]
    assert len(briefing["next_steps"]) >= 2
    assert any("risk" in step.lower() or "renewal" in step.lower() or "expansion" in step.lower() for step in briefing["next_steps"])
