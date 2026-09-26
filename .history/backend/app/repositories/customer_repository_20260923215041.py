from __future__ import annotations

from typing import Any

from app.db.domain.customer.customer import Customer
from app.db.session import SessionLocal, init_db


class CustomerRepository:
    _store: dict[str, dict[str, Any]] = {}

    def __init__(self) -> None:
        self._store = self.__class__._store
        init_db()
        self._reload_from_db()

    def _reload_from_db(self) -> None:
        with SessionLocal() as session:
            rows = session.query(Customer).all()

        grouped: dict[str, dict[str, dict[str, Any]]] = {}
        for row in rows:
            grouped.setdefault(row.organization_id, {})[row.id] = {
                "id": row.id,
                "organization_id": row.organization_id,
                "name": row.name,
                "email": row.email,
                "company": row.company,
                "status": row.status,
                "health_score": row.health_score,
                "risk_level": row.risk_level,
                "monthly_revenue": row.monthly_revenue,
                "segment": row.segment,
                "last_interaction": row.last_interaction,
            }
        self._store = grouped

    def list_for_organization(self, organization_id: str) -> list[dict[str, Any]]:
        self._reload_from_db()
        return list(self._store.get(organization_id, {}).values())

    def get_by_email(self, organization_id: str, email: str) -> dict[str, Any] | None:
        normalized_email = email.lower().strip()
        for customer in self.list_for_organization(organization_id):
            if customer.get("email", "").lower().strip() == normalized_email:
                return customer
        return None

    def upsert(self, customer: dict[str, Any]) -> dict[str, Any]:
        with SessionLocal() as session:
            row = session.query(Customer).filter(Customer.id == customer["id"]).one_or_none()
            if row is None:
                row = Customer(
                    id=customer["id"],
                    organization_id=customer["organization_id"],
                    name=customer["name"],
                    email=customer["email"].lower().strip(),
                    company=customer.get("company"),
                    status=customer.get("status", "Healthy"),
                    health_score=customer.get("health_score", 100),
                    risk_level=customer.get("risk_level", "Low"),
                    monthly_revenue=customer.get("monthly_revenue", 0.0),
                    segment=customer.get("segment", "Unknown"),
                    last_interaction=customer.get("last_interaction", "N/A"),
                )
                session.add(row)
            else:
                row.organization_id = customer["organization_id"]
                row.name = customer["name"]
                row.email = customer["email"].lower().strip()
                row.company = customer.get("company")
                row.status = customer.get("status", "Healthy")
                row.health_score = customer.get("health_score", 100)
                row.risk_level = customer.get("risk_level", "Low")
                row.monthly_revenue = customer.get("monthly_revenue", 0.0)
                row.segment = customer.get("segment", "Unknown")
                row.last_interaction = customer.get("last_interaction", "N/A")
            session.commit()

        self._reload_from_db()
        return customer

    def all(self) -> dict[str, dict[str, dict[str, Any]]]:
        self._reload_from_db()
        return dict(self._store)
