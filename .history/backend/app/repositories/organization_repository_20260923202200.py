from __future__ import annotations

from typing import Any


class OrganizationRepository:
    _store: dict[str, dict[str, Any]] = {}

    def __init__(self) -> None:
        self._store = self.__class__._store

    def get_by_id(self, organization_id: str) -> dict[str, Any] | None:
        return self._store.get(organization_id)

    def create(self, organization: dict[str, Any]) -> dict[str, Any]:
        self._store[organization["id"]] = organization
        return organization

    def all(self) -> dict[str, dict[str, Any]]:
        return dict(self._store)
