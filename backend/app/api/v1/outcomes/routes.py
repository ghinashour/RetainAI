from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.authz import require_organization_scope
from app.core.exceptions import NotFoundError
from app.repositories.customer_repository import CustomerRepository
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.outcome_repository import OutcomeRepository

router = APIRouter(prefix="/outcomes", tags=["outcomes"])


class OutcomeCreateRequest(BaseModel):
    customer_id: str
    status: str
    value: float | None = None
    note: str | None = None


@router.post("")
def create_outcome(
    payload: OutcomeCreateRequest,
    current_user: dict[str, Any] = Depends(require_organization_scope),
) -> dict[str, Any]:
    organization_id = current_user.get("organization_id") or current_user.get("org_id")
    organization = OrganizationRepository().get_by_id(organization_id)
    organization_name = organization.get("name") if organization else "Workspace"

    customers = CustomerRepository().list_for_organization(organization_id)
    if not any(customer.get("id") == payload.customer_id for customer in customers):
        raise NotFoundError("Customer not found for this organization")

    outcome = {
        "id": str(uuid.uuid4()),
        "organization_id": organization_id,
        "customer_id": payload.customer_id,
        "status": payload.status,
        "value": payload.value or 0.0,
        "note": payload.note or "",
    }
    OutcomeRepository().create(outcome)

    return {
        "organization_name": organization_name,
        "outcome": outcome,
    }


@router.get("")
def list_outcomes(current_user: dict[str, Any] = Depends(require_organization_scope)) -> dict[str, Any]:
    organization_id = current_user.get("organization_id") or current_user.get("org_id")
    organization = OrganizationRepository().get_by_id(organization_id)
    organization_name = organization.get("name") if organization else "Workspace"
    outcomes = OutcomeRepository().list_for_organization(organization_id)

    return {
        "organization_name": organization_name,
        "outcomes": outcomes,
    }
