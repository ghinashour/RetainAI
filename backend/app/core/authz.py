from typing import Any

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import AuthorizationError
from app.core.security import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if credentials is None:
        raise AuthorizationError("Authentication required")
    return credentials.credentials


def require_authenticated_user(
    token: str = Depends(get_current_user_token),
) -> dict[str, Any]:
    payload = decode_token(token)
    return payload


def require_organization_scope(
    user_payload: dict[str, Any] = Depends(require_authenticated_user),
) -> dict[str, Any]:
    organization_id = user_payload.get("organization_id") or user_payload.get("org_id")
    if not organization_id:
        raise AuthorizationError("Authenticated user is not associated with an organization")
    return user_payload
