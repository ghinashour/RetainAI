from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.authz import require_organization_scope
from app.repositories.organization_repository import OrganizationRepository
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("")
def list_customers(current_user: dict = Depends(require_organization_scope)) -> dict:
    organization_id = current_user.get("organization_id") or current_user.get("org_id")
    organization_name = OrganizationRepository().get_by_id(organization_id).get("name") if OrganizationRepository().get_by_id(organization_id) else "Workspace"
    customers = CustomerService().list_customers(organization_id)

    return {
        "organization_name": organization_name,
        "customers": customers,
    }
