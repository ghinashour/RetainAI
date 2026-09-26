from __future__ import annotations

from typing import Any

from app.repositories.customer_repository import CustomerRepository
from app.services.analytics_service import AnalyticsService
from app.services.recommendation_service import RecommendationService


class AssistantService:
    def get_briefing(self, organization_id: str | None, organization_name: str) -> dict[str, Any]:
        customers = CustomerRepository().list_for_organization(organization_id) if organization_id else []
        analytics = AnalyticsService().get_summary(organization_id)
        recommendations = RecommendationService().list_recommendations(organization_id)

        top_risks = [
            customer.get("name", "Unnamed customer")
            for customer in sorted(customers, key=lambda item: int(item.get("health_score", 100)))[:3]
            if int(customer.get("health_score", 100)) < 60
        ]

        headline = (
            f"{organization_name} is tracking {analytics['at_risk_customers']} at-risk accounts and "
            f"{analytics['critical_customers']} critical accounts."
        )

        risk_summary = (
            f"Retention risk is concentrated in {', '.join(top_risks) if top_risks else 'your current portfolio'}; "
            f"the current retention score is {analytics['retention_score']}/100."
        )

        next_steps = [
            f"Prioritize renewal recovery outreach for {analytics['critical_customers']} critical customers.",
            "Launch a focused intervention plan for at-risk accounts with the weakest health scores.",
        ]
        if recommendations:
            next_steps.append(recommendations[0].get("next_step", "Review the top recommendation in the recommendation feed."))

        return {
            "organization_name": organization_name,
            "headline": headline,
            "risk_summary": risk_summary,
            "next_steps": next_steps[:3],
            "top_risk_customers": top_risks,
            "summary": analytics,
        }
