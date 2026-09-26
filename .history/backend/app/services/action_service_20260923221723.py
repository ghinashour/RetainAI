from __future__ import annotations

from typing import Any

from app.repositories.customer_repository import CustomerRepository


class ActionService:
    def list_actions(self, organization_id: str | None) -> list[dict[str, Any]]:
        if not organization_id:
            return self._fallback_actions()

        customers = CustomerRepository().list_for_organization(organization_id)
        actions: list[dict[str, Any]] = []

        for customer in sorted(customers, key=lambda item: int(item.get("health_score", 100)))[:5]:
            health_score = int(customer.get("health_score", 100))
            if health_score < 35:
                actions.append(
                    {
                        "id": f"action-critical-{customer['id']}",
                        "title": f"Review critical customer: {customer['name']} ({health_score}/100)",
                        "priority": "High",
                        "due_in": "Today",
                        "owner": "CS Ops",
                    }
                )
            elif health_score < 60:
                actions.append(
                    {
                        "id": f"action-risk-{customer['id']}",
                        "title": f"Schedule proactive outreach with {customer['name']} ({health_score}/100)",
                        "priority": "Medium",
                        "due_in": "2 days",
                        "owner": "Account team",
                    }
                )

        if not actions:
            return self._fallback_actions()

        return actions[:5]

    @staticmethod
    def _fallback_actions() -> list[dict[str, Any]]:
        return [
            {
                "id": "action-1",
                "title": "Review critical customers",
                "priority": "High",
                "due_in": "Today",
                "owner": "CS Ops",
            },
            {
                "id": "action-2",
                "title": "Schedule renewal follow-up",
                "priority": "High",
                "due_in": "2 days",
                "owner": "Account team",
            },
            {
                "id": "action-3",
                "title": "Audit recent churn signals in onboarding funnel",
                "priority": "Medium",
                "due_in": "This week",
                "owner": "Data team",
            },
        ]
