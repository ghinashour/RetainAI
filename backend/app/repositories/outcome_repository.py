from __future__ import annotations

from typing import Any


class OutcomeRepository:
    _store: dict[str, dict[str, dict[str, Any]]] = {}

    def __init__(self) -> None:
        self._store = self.__class__._store

    def list_for_organization(self, organization_id: str) -> list[dict[str, Any]]:
        return list(self._store.get(organization_id, {}).values())

    def create(self, outcome: dict[str, Any]) -> dict[str, Any]:
        organization_id = outcome["organization_id"]
        self._store.setdefault(organization_id, {})
        self._store[organization_id][outcome["id"]] = outcome
        return outcome

    def all(self) -> dict[str, dict[str, dict[str, Any]]]:
        return dict(self._store)
