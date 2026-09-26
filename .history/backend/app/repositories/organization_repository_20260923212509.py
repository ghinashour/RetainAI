from __future__ import annotations

from typing import Any

from app.db.domain.organization.organization import Organization
from app.db.session import SessionLocal, init_db


class OrganizationRepository:
    _store: dict[str, dict[str, Any]] = {}

    def __init__(self) -> None:
        self._store = self.__class__._store
        init_db()
        self._reload_from_db()

    def _reload_from_db(self) -> None:
        with SessionLocal() as session:
            rows = session.query(Organization).all()
        self._store = {
            row.id: {
                "id": row.id,
                "name": row.name,
                "slug": row.slug,
                "is_active": row.is_active,
            }
            for row in rows
        }

    def get_by_id(self, organization_id: str) -> dict[str, Any] | None:
        if organization_id in self._store:
            return self._store[organization_id]
        with SessionLocal() as session:
            row = session.query(Organization).filter(Organization.id == organization_id).one_or_none()
        if row is None:
            return None
        payload = {
            "id": row.id,
            "name": row.name,
            "slug": row.slug,
            "is_active": row.is_active,
        }
        self._store[organization_id] = payload
        return payload

    def create(self, organization: dict[str, Any]) -> dict[str, Any]:
        with SessionLocal() as session:
            row = session.query(Organization).filter(Organization.id == organization["id"]).one_or_none()
            if row is None:
                row = Organization(
                    id=organization["id"],
                    name=organization["name"],
                    slug=organization.get("slug"),
                    is_active=organization.get("is_active", True),
                )
                session.add(row)
            else:
                row.name = organization["name"]
                row.slug = organization.get("slug")
                row.is_active = organization.get("is_active", True)
            session.commit()
        self._store[organization["id"]] = organization
        return organization

    def all(self) -> dict[str, dict[str, Any]]:
        self._reload_from_db()
        return dict(self._store)
