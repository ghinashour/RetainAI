from dataclasses import dataclass
from typing import Protocol


class AuthUser(Protocol):
    id: str
    email: str
    organization_id: str | None


@dataclass
class AuthContext:
    user_id: str
    email: str
    organization_id: str | None = None


class AuthService:
    def __init__(self) -> None:
        pass

    def build_context(self, user: AuthUser) -> AuthContext:
        return AuthContext(
            user_id=user.id,
            email=user.email,
            organization_id=user.organization_id,
        )
