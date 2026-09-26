from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.core.authz import require_organization_scope
from app.repositories.organization_repository import OrganizationRepository
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary")
def get_analytics_summary(current_user: dict[str, Any] = Depends(require_organization_scope)) -> dict[str, Any]:
    organization_id = current_user.get("organization_id") or current_user.get("org_id")
    organization = OrganizationRepository().get_by_id(organization_id)
    organization_name = organization.get("name") if organization else "Workspace"
    return {
        "organization_name": organization_name,
        "summary": AnalyticsService().get_summary(organization_id),
    }
