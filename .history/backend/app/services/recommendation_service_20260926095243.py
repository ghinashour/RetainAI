from __future__ import annotations

from typing import Any

from app.repositories.customer_repository import CustomerRepository
from app.services.ai_analysis_service import AIAnalysisService
from app.services.analytics_service import AnalyticsService


class RecommendationService:
    def list_recommendations(self, organization_id: str | None) -> list[dict[str, Any]]:
        return self.get_analysis(organization_id)["recommendations"]

    def get_analysis(self, organization_id: str | None) -> dict[str, Any]:
        customers = CustomerRepository().list_for_organization(organization_id) if organization_id else []
        metrics = AnalyticsService().get_summary(organization_id)
        return AIAnalysisService().analyze_portfolio("Customer portfolio", customers, metrics)
