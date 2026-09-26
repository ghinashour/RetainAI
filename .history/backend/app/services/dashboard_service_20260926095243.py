from __future__ import annotations

from typing import Any

from app.repositories.customer_repository import CustomerRepository


class DashboardService:
    def get_overview(self, *, organization_id: str, organization_name: str) -> dict[str, Any]:
        customers = CustomerRepository().list_for_organization(organization_id)

        total_customers = len(customers)
        critical_customers = sum(1 for customer in customers if customer.get("status") == "Critical")
        at_risk_customers = sum(1 for customer in customers if customer.get("status") == "At risk")
        revenue_at_risk = sum(
            float(customer.get("monthly_revenue", 0))
            for customer in customers
            if customer.get("status") in {"At risk", "Critical"}
        )

        return {
            "organization": {
                "id": organization_id,
                "name": organization_name,
            },
            "snapshot": {
                "total_customers": total_customers,
                "at_risk_customers": at_risk_customers,
                "critical_customers": critical_customers,
                "revenue_at_risk": round(revenue_at_risk),
                "currency": "USD",
            },
            "priority_actions": [],
        }
