from __future__ import annotations

from typing import Any


class CustomerService:
    def list_customers(self, organization_id: str | None) -> list[dict[str, Any]]:
        _ = organization_id
        return [
            {
                "id": "cust-1001",
                "name": "Alicia Bennett",
                "email": "alicia@northwindlabs.com",
                "status": "Critical",
                "health_score": 32,
                "risk_level": "High",
                "monthly_revenue": 18200,
                "last_interaction": "2 days ago",
                "segment": "Enterprise",
            },
            {
                "id": "cust-1002",
                "name": "Paul Nguyen",
                "email": "paul@harborwest.io",
                "status": "At risk",
                "health_score": 48,
                "risk_level": "Medium",
                "monthly_revenue": 9600,
                "last_interaction": "5 days ago",
                "segment": "SMB",
            },
            {
                "id": "cust-1003",
                "name": "Mira Patel",
                "email": "mira@violetworks.com",
                "status": "Healthy",
                "health_score": 86,
                "risk_level": "Low",
                "monthly_revenue": 14300,
                "last_interaction": "1 day ago",
                "segment": "Growth",
            },
        ]
