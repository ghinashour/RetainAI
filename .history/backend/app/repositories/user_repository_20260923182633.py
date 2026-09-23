from __future__ import annotations

from typing import Any


class UserRepository:
    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = {}

    def get_by_email(self, email: str) -> dict[str, Any] | None:
        return self._store.get(email.lower().strip())

    def get_by_id(self, user_id: str) -> dict[str, Any] | None:
        for user in self._store.values():
            if user.get("id") == user_id:
                return user
        return None

    def create(self, user: dict[str, Any]) -> dict[str, Any]:
        normalized_email = user["email"].lower().strip()
        self._store[normalized_email] = user
        return user

    def all(self) -> dict[str, dict[str, Any]]:
        return dict(self._store)
