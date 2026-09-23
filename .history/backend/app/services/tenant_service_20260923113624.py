from typing import Protocol


class OrganizationContext(Protocol):
    organization_id: str | None


def require_organization_context(user: OrganizationContext) -> str:
    if not user or not getattr(user, "organization_id", None):
        raise ValueError("Authenticated user must belong to an organization")
    return user.organization_id
