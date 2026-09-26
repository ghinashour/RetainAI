from __future__ import annotations

from typing import Any


class InterventionRepository:
    _store: dict[str, dict[str, dict[str, Any]]] = {}

    def __init__(self) -> None:
        self._store = self.__class__._store

    def list_for_organization(self, organization_id: str) -> list[dict[str, Any]]:
        return list(self._store.get(organization_id, {}).values())

    def create(self, intervention: dict[str, Any]) -> dict[str, Any]:
        organization_id = intervention["organization_id"]
        self._store.setdefault(organization_id, {})
        self._store[organization_id][intervention["id"]] = intervention
        return intervention

    def all(self) -> dict[str, dict[str, dict[str, Any]]]:
        return dict(self._store)
