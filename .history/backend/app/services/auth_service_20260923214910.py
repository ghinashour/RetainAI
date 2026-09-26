import uuid
from dataclasses import dataclass
from typing import Any, Protocol

from app.core.exceptions import AuthenticationError, ValidationError
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.user_repository import UserRepository


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
    _users_by_email: dict[str, dict[str, Any]] = {}
    _organizations_by_id: dict[str, dict[str, Any]] = {}

    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.organization_repository = OrganizationRepository()
        self._users_by_email = self.user_repository._store
        self._organizations_by_id = self.organization_repository._store
        self._seed_demo_user_if_needed()

    def _seed_demo_user_if_needed(self) -> None:
        if "test@example.com" not in self._users_by_email:
            organization_id = str(uuid.uuid4())
            user_id = str(uuid.uuid4())
            self.organization_repository.create(
                {
                    "id": organization_id,
                    "name": "Demo Org",
                    "slug": "demo-org",
                    "is_active": True,
                }
            )
            self.user_repository.create(
                {
                    "id": user_id,
                    "email": "test@example.com",
                    "password_hash": hash_password("Password123!"),
                    "full_name": None,
                    "organization_id": organization_id,
                    "is_active": True,
                }
            )

    def register_user(self, email: str, password: str, organization_name: str) -> dict[str, Any]:
        normalized_email = email.lower().strip()
        if not normalized_email:
            raise ValidationError("Email is required")
        if normalized_email in self._users_by_email:
            raise ValidationError("An account with this email already exists")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        organization_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        name = organization_name.strip()
        base_slug = name.lower().replace(" ", "-") or "organization"
        slug = base_slug
        suffix = 1
        while self.organization_repository.get_by_slug(slug) is not None:
            slug = f"{base_slug}-{suffix}"
            suffix += 1
        organization_payload = {
            "id": organization_id,
            "name": name,
            "slug": slug,
            "is_active": True,
        }
        self.organization_repository.create(organization_payload)

        new_user = {
            "id": user_id,
            "email": normalized_email,
            "password_hash": hash_password(password),
            "full_name": None,
            "organization_id": organization_id,
            "is_active": True,
        }
        self.user_repository.create(new_user)

        return self._users_by_email[normalized_email]

    def authenticate_user(self, email: str, password: str) -> dict[str, Any]:
        normalized_email = email.lower().strip()
        user = self._users_by_email.get(normalized_email)
        if user is None or not verify_password(password, user["password_hash"]):
            raise AuthenticationError("Invalid email or password")
        return user

    def build_context(self, user: AuthUser) -> AuthContext:
        return AuthContext(
            user_id=user.id,
            email=user.email,
            organization_id=user.organization_id,
        )

    def get_user_payload(self, user: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user.get("full_name"),
            "organization_id": user.get("organization_id"),
        }

    def build_tokens(self, user: dict[str, Any]) -> dict[str, str]:
        organization_id = user.get("organization_id")
        return {
            "access_token": create_access_token(user["id"], organization_id=organization_id),
            "refresh_token": create_refresh_token(user["id"], organization_id=organization_id),
            "token_type": "bearer",
        }
