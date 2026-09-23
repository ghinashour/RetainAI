from typing import Any

from fastapi import APIRouter, Depends

from app.core.authz import require_authenticated_user
from app.core.exceptions import AuthenticationError, ValidationError
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
service = AuthService()


@router.post("/register", status_code=201)
def register(payload: RegisterRequest) -> dict[str, Any]:
    user = service.register_user(payload.email, payload.password, payload.organization_name)
    organization = service._organizations_by_id[user["organization_id"]]
    tokens = service.build_tokens(user)
    return {
        "user": service.get_user_payload(user),
        "organization": {
            "id": organization["id"],
            "name": organization["name"],
            "slug": organization.get("slug"),
            "is_active": organization.get("is_active", True),
        },
        "tokens": TokenResponse(**tokens).model_dump(),
    }


@router.post("/login")
def login(payload: LoginRequest) -> dict[str, Any]:
    user = service.authenticate_user(payload.email, payload.password)
    tokens = service.build_tokens(user)
    return {
        "user": service.get_user_payload(user),
        "tokens": TokenResponse(**tokens).model_dump(),
    }


@router.post("/refresh")
def refresh(payload: dict[str, str]) -> dict[str, Any]:
    token = payload.get("refresh_token")
    if not token:
        raise ValidationError("Refresh token is required")
    claims = decode_token(token)
    if claims.get("type") != "refresh":
        raise AuthenticationError("Invalid refresh token")
    user = service._users_by_email.get(claims.get("sub", ""))
    if user is None:
        raise AuthenticationError("User no longer exists")
    tokens = service.build_tokens(user)
    return {"user": service.get_user_payload(user), "tokens": TokenResponse(**tokens).model_dump()}


@router.get("/me")
def me(current_user: dict[str, Any] = Depends(require_authenticated_user)) -> dict[str, Any]:
    user = service._users_by_email.get(current_user.get("sub", ""))
    if user is None:
        raise AuthenticationError("User not found")
    return {"user": service.get_user_payload(user)}
