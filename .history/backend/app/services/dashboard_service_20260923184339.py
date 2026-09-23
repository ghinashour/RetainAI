from __future__ import annotations

from typing import Any


class DashboardService:
    def get_overview(self, *, organization_id: str, organization_name: str) -> dict[str, Any]:
        return {
            "organization": {
                "id": organization_id,
                "name": organization_name,
            },
            "snapshot": {
                "total_customers": 1248,
                "at_risk_customers": 143,
                "critical_customers": 27,
                "revenue_at_risk": 184600,
                "currency": "USD",
            },
            "priority_actions": [
                "Review 27 critical customers",
                "Schedule 6 intervention follow-ups",
                "Audit recent data imports",
            ],
        }
