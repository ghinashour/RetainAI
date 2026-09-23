from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.authz import require_organization_scope
from app.repositories.organization_repository import OrganizationRepository
from app.services.action_service import ActionService

router = APIRouter(prefix="/actions", tags=["actions"])


@router.get("")
def list_actions(current_user: dict = Depends(require_organization_scope)) -> dict:
    organization_id = current_user.get("organization_id") or current_user.get("org_id")
    organization = OrganizationRepository().get_by_id(organization_id)
    organization_name = organization.get("name") if organization else "Workspace"
    return {
        "organization_name": organization_name,
        "actions": ActionService().list_actions(organization_id),
    }
