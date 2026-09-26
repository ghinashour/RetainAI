from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.authz import require_organization_scope
from app.core.exceptions import NotFoundError
from app.repositories.customer_repository import CustomerRepository
from app.repositories.intervention_repository import InterventionRepository
from app.repositories.organization_repository import OrganizationRepository

router = APIRouter(prefix="/interventions", tags=["interventions"])


class InterventionCreateRequest(BaseModel):
    customer_id: str
    title: str
    channel: str = "email"
    status: str = "scheduled"
    notes: str | None = None
    due_in: str | None = None
    owner: str | None = None


@router.post("")
def create_intervention(
    payload: InterventionCreateRequest,
    current_user: dict[str, Any] = Depends(require_organization_scope),
) -> dict[str, Any]:
    organization_id = current_user.get("organization_id") or current_user.get("org_id")
    organization = OrganizationRepository().get_by_id(organization_id)
    organization_name = organization.get("name") if organization else "Workspace"

    customers = CustomerRepository().list_for_organization(organization_id)
    if not any(customer.get("id") == payload.customer_id for customer in customers):
        raise NotFoundError("Customer not found for this organization")

    intervention = {
        "id": str(uuid.uuid4()),
        "organization_id": organization_id,
        "customer_id": payload.customer_id,
        "title": payload.title,
        "channel": payload.channel,
        "status": payload.status,
        "notes": payload.notes,
        "due_in": payload.due_in or "7 days",
        "owner": payload.owner or "CS Ops",
    }
    InterventionRepository().create(intervention)

    return {
        "organization_name": organization_name,
        "intervention": intervention,
    }


@router.get("")
def list_interventions(current_user: dict[str, Any] = Depends(require_organization_scope)) -> dict[str, Any]:
    organization_id = current_user.get("organization_id") or current_user.get("org_id")
    organization = OrganizationRepository().get_by_id(organization_id)
    organization_name = organization.get("name") if organization else "Workspace"
    interventions = InterventionRepository().list_for_organization(organization_id)

    return {
        "organization_name": organization_name,
        "interventions": interventions,
    }
