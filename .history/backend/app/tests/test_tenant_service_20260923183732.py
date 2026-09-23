import pytest

from app.core.authz import require_organization_scope
from app.core.exceptions import AuthorizationError
from app.services.tenant_service import TenantService


class UserWithOrg:
    def __init__(self, organization_id):
        self.organization_id = organization_id


def test_tenant_service_returns_organization_id_for_valid_context() -> None:
    service = TenantService()
    org_id = service.require_organization_context(UserWithOrg("org-123"))
    assert org_id == "org-123"


def test_tenant_service_rejects_missing_organization_context() -> None:
    service = TenantService()
    with pytest.raises(AuthorizationError):
        service.require_organization_context(UserWithOrg(None))


def test_require_organization_scope_accepts_organization_id_payload() -> None:
    payload = {"sub": "user-1", "organization_id": "org-123"}

    result = require_organization_scope(payload)

    assert result == payload
