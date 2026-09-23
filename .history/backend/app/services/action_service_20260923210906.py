from __future__ import annotations

from typing import Any


class ActionService:
    def list_actions(self, organization_id: str | None) -> list[dict[str, Any]]:
        _ = organization_id
        return [
            {
                "id": "action-1",
                "title": "Review 27 critical customers",
                "priority": "High",
                "due_in": "Today",
                "owner": "CS Ops",
            },
            {
                "id": "action-2",
                "title": "Schedule renewal follow-up for Harbor West",
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
