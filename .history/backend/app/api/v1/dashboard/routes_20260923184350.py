from typing import Any

from fastapi import APIRouter, Depends

from app.core.authz import require_organization_scope
from app.services.auth_service import AuthService
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview")
def get_dashboard_overview(current_user: dict[str, Any] = Depends(require_organization_scope)) -> dict[str, Any]:
    organization_id = current_user.get("organization_id") or current_user.get("org_id")
    auth_service = AuthService()
    organization = auth_service.organization_repository.get_by_id(organization_id)
    if organization is None:
        raise ValueError("Organization not found for the current user")

    dashboard_service = DashboardService()
    return dashboard_service.get_overview(
        organization_id=organization_id,
        organization_name=organization.get("name", "Organization"),
    )
