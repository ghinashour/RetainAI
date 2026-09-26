from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.core.authz import require_organization_scope
from app.repositories.organization_repository import OrganizationRepository
from app.services.assistant_service import AssistantService

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.get("/briefing")
def get_assistant_briefing(current_user: dict[str, Any] = Depends(require_organization_scope)) -> dict[str, Any]:
    organization_id = current_user.get("organization_id") or current_user.get("org_id")
    organization = OrganizationRepository().get_by_id(organization_id)
    organization_name = organization.get("name") if organization else "Workspace"
    return AssistantService().get_briefing(organization_id, organization_name)
