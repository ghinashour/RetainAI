from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.authz import require_organization_scope
from app.repositories.organization_repository import OrganizationRepository
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


class CustomerImportRequest(BaseModel):
    csv: str | None = None
    customers: list[dict[str, Any]] | None = None


@router.get("")
def list_customers(current_user: dict = Depends(require_organization_scope)) -> dict:
    organization_id = current_user.get("organization_id") or current_user.get("org_id")
    organization = OrganizationRepository().get_by_id(organization_id)
    organization_name = organization.get("name") if organization else "Workspace"
    customers = CustomerService().list_customers(organization_id)

    return {
        "organization_name": organization_name,
        "customers": customers,
    }


@router.post("/import")
def import_customers(
    payload: CustomerImportRequest,
    current_user: dict = Depends(require_organization_scope),
) -> dict:
    organization_id = current_user.get("organization_id") or current_user.get("org_id")
    organization = OrganizationRepository().get_by_id(organization_id)
    organization_name = organization.get("name") if organization else "Workspace"
    imported = CustomerService().import_customers(organization_id, payload.csv, payload.customers)

    return {
        "organization_name": organization_name,
        "created": len(imported),
        "customers": imported,
    }
