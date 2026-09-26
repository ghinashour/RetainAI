from __future__ import annotations

from typing import Any

from app.repositories.customer_repository import CustomerRepository
from app.services.ai_analysis_service import AIAnalysisService
from app.services.analytics_service import AnalyticsService


class ActionService:
    def list_actions(self, organization_id: str | None) -> list[dict[str, Any]]:
        return self.get_analysis(organization_id)["actions"]

    def get_analysis(self, organization_id: str | None) -> dict[str, Any]:
        customers = CustomerRepository().list_for_organization(organization_id) if organization_id else []
        if not customers:
            return {
                "available": False,
                "status": "no_data",
                "message": "Import customer data to generate AI actions.",
                "actions": self._fallback_actions(),
            }

        analysis = AIAnalysisService().analyze_portfolio(
            "Customer portfolio",
            customers,
            AnalyticsService().get_summary(organization_id),
        )
        return {
            "available": analysis["available"],
            "status": analysis["status"],
            "message": analysis["message"],
            "actions": analysis["recommendations"] if analysis["available"] else [],
        }

    @staticmethod
    def _fallback_actions() -> list[dict[str, Any]]:
        return [
            {
                "id": "action-1",
                "title": "Import customer data to enable analysis",
                "priority": "Info",
                "reason": "There are no customer records in this workspace.",
                "next_step": "Import an authorized customer CSV from the Customers view.",
            },
            {
                "id": "action-2",
                "title": "Configure an AI provider",
                "priority": "Info",
                "reason": "AI-generated recommendations require a configured model provider.",
                "next_step": "Set AI_API_KEY and restart the backend.",
            },
        ]
