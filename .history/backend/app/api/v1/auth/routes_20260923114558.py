from fastapi import APIRouter

from app.core.exceptions import RetainAIError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register_placeholder() -> dict[str, str]:
    raise RetainAIError("Authentication registration is not implemented yet in Phase 1", code="NOT_IMPLEMENTED")


@router.post("/login")
def login_placeholder() -> dict[str, str]:
    raise RetainAIError("Authentication login is not implemented yet in Phase 1", code="NOT_IMPLEMENTED")


@router.post("/refresh")
def refresh_placeholder() -> dict[str, str]:
    raise RetainAIError("Authentication refresh is not implemented yet in Phase 1", code="NOT_IMPLEMENTED")


@router.get("/me")
def me_placeholder() -> dict[str, str]:
    raise RetainAIError("Authenticated user profile is not implemented yet in Phase 1", code="NOT_IMPLEMENTED")
