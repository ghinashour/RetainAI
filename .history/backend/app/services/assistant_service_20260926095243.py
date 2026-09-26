from __future__ import annotations

from typing import Any

from app.services.analytics_service import AnalyticsService
from app.repositories.customer_repository import CustomerRepository
from app.services.ai_analysis_service import AIAnalysisService


class AssistantService:
    def get_briefing(self, organization_id: str | None, organization_name: str) -> dict[str, Any]:
        customers = CustomerRepository().list_for_organization(organization_id) if organization_id else []
        analytics = AnalyticsService().get_summary(organization_id)
        analysis = AIAnalysisService().analyze_portfolio(organization_name, customers, analytics)
        return {
            "organization_name": organization_name,
            "summary": analytics,
            **analysis,
        }
