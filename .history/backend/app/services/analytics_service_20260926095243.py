from __future__ import annotations

from typing import Any

from app.repositories.customer_repository import CustomerRepository
from app.repositories.intervention_repository import InterventionRepository
from app.repositories.outcome_repository import OutcomeRepository


class AnalyticsService:
    def get_summary(self, organization_id: str | None) -> dict[str, Any]:
        customers = CustomerRepository().list_for_organization(organization_id) if organization_id else []
        interventions = InterventionRepository().list_for_organization(organization_id) if organization_id else []
        outcomes = OutcomeRepository().list_for_organization(organization_id) if organization_id else []

        total_customers = len(customers)
        critical_customers = sum(1 for customer in customers if customer.get("status") == "Critical")
        at_risk_customers = sum(1 for customer in customers if customer.get("status") == "At risk")
        healthy_customers = sum(1 for customer in customers if customer.get("status") == "Healthy")
        revenue_at_risk = sum(
            float(customer.get("monthly_revenue", 0))
            for customer in customers
            if customer.get("status") in {"At risk", "Critical"}
        )
        positive_outcomes = sum(1 for outcome in outcomes if str(outcome.get("status", "")).lower() == "positive")
        scheduled_interventions = sum(
            1
            for intervention in interventions
            if str(intervention.get("status", "")).lower() in {"scheduled", "in_progress", "pending"}
        )

        return {
            "total_customers": total_customers,
            "healthy_customers": healthy_customers,
            "at_risk_customers": at_risk_customers,
            "critical_customers": critical_customers,
            "revenue_at_risk": round(revenue_at_risk),
            "currency": "USD",
            "positive_outcomes": positive_outcomes,
            "scheduled_interventions": scheduled_interventions,
        }
