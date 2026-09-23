from app.repositories.organization_repository import OrganizationRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def test_user_repository_tracks_normalized_emails() -> None:
    repo = UserRepository()
    user = {
        "id": "user-1",
        "email": "Test@Example.com",
        "password_hash": "hashed",
        "organization_id": "org-1",
    }

    repo.create(user)

    assert repo.get_by_email("test@example.com") == user
    assert repo.get_by_id("user-1") == user


def test_auth_service_uses_repository_backing_store() -> None:
    service = AuthService()
    service.user_repository.create(
        {
            "id": "user-2",
            "email": "alice@example.com",
            "password_hash": service.user_repository.get_by_email("test@example.com")["password_hash"],
            "organization_id": "org-2",
        }
    )

    assert service._users_by_email["alice@example.com"]["id"] == "user-2"
    assert service._organizations_by_id == service.organization_repository.all()
