from __future__ import annotations

from typing import Any

from app.repositories.customer_repository import CustomerRepository


class RecommendationService:
    def list_recommendations(self, organization_id: str | None) -> list[dict[str, Any]]:
        if not organization_id:
            return self._fallback_recommendations()

        customers = CustomerRepository().list_for_organization(organization_id)
        recommendations: list[dict[str, Any]] = []

        for customer in sorted(customers, key=lambda item: (int(item.get("health_score", 100)), item.get("name", "")))[:10]:
            health_score = int(customer.get("health_score", 100))
            if health_score < 35:
                recommendations.append(
                    {
                        "id": f"recommendation-critical-{customer['id']}",
                        "customer_id": customer["id"],
                        "customer_name": customer["name"],
                        "title": f"Renewal recovery plan for {customer['name']} ({health_score}/100)",
                        "priority": "High",
                        "reason": "Critical health score and strong risk of churn.",
                        "next_step": "Launch a renewal recovery playbook with executive sponsor outreach.",
                    }
                )
            elif health_score < 60:
                recommendations.append(
                    {
                        "id": f"recommendation-risk-{customer['id']}",
                        "customer_id": customer["id"],
                        "customer_name": customer["name"],
                        "title": f"Expansion outreach for {customer['name']} ({health_score}/100)",
                        "priority": "Medium",
                        "reason": "Customer is showing early retention risk and expansion opportunity.",
                        "next_step": "Schedule a usage review and tailored renewal offer within 48 hours.",
                    }
                )

        if not recommendations:
            return self._fallback_recommendations()

        return recommendations[:5]

    @staticmethod
    def _fallback_recommendations() -> list[dict[str, Any]]:
        return [
            {
                "id": "recommendation-1",
                "customer_id": "",
                "customer_name": "All customers",
                "title": "Renewal follow-up for at-risk accounts",
                "priority": "High",
                "reason": "Prioritize the accounts with the lowest health scores.",
                "next_step": "Review discount thresholds and customer success engagement plans.",
            },
            {
                "id": "recommendation-2",
                "customer_id": "",
                "customer_name": "Expansion pipeline",
                "title": "Expansion plan for healthy growth accounts",
                "priority": "Medium",
                "reason": "Accounts with positive momentum can unlock additional adoption.",
                "next_step": "Bundle onboarding improvements and offer a product adoption review.",
            },
        ]
