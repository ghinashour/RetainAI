from typing import Protocol

from app.core.exceptions import AuthorizationError


class OrganizationContext(Protocol):
    organization_id: str | None


class TenantService:
    def require_organization_context(self, user: OrganizationContext) -> str:
        if not user or not getattr(user, "organization_id", None):
            raise AuthorizationError("Authenticated user must belong to an organization")
        return user.organization_id
