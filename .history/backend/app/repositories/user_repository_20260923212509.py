from __future__ import annotations

from typing import Any

from app.db.domain.auth.user import User
from app.db.session import SessionLocal, init_db


class UserRepository:
    _store: dict[str, dict[str, Any]] = {}

    def __init__(self) -> None:
        self._store = self.__class__._store
        init_db()
        self._reload_from_db()

    def _reload_from_db(self) -> None:
        with SessionLocal() as session:
            rows = session.query(User).all()
        self._store = {
            row.email.lower().strip(): {
                "id": row.id,
                "email": row.email,
                "password_hash": row.password_hash,
                "full_name": row.full_name,
                "organization_id": row.organization_id,
                "is_active": row.is_active,
            }
            for row in rows
        }

    def get_by_email(self, email: str) -> dict[str, Any] | None:
        normalized_email = email.lower().strip()
        if normalized_email in self._store:
            return self._store[normalized_email]
        with SessionLocal() as session:
            row = session.query(User).filter(User.email == normalized_email).one_or_none()
        if row is None:
            return None
        payload = {
            "id": row.id,
            "email": row.email,
            "password_hash": row.password_hash,
            "full_name": row.full_name,
            "organization_id": row.organization_id,
            "is_active": row.is_active,
        }
        self._store[normalized_email] = payload
        return payload

    def get_by_id(self, user_id: str) -> dict[str, Any] | None:
        for user in self._store.values():
            if user.get("id") == user_id:
                return user
        with SessionLocal() as session:
            row = session.query(User).filter(User.id == user_id).one_or_none()
        if row is None:
            return None
        payload = {
            "id": row.id,
            "email": row.email,
            "password_hash": row.password_hash,
            "full_name": row.full_name,
            "organization_id": row.organization_id,
            "is_active": row.is_active,
        }
        self._store[row.email.lower().strip()] = payload
        return payload

    def create(self, user: dict[str, Any]) -> dict[str, Any]:
        normalized_email = user["email"].lower().strip()
        with SessionLocal() as session:
            row = session.query(User).filter(User.email == normalized_email).one_or_none()
            if row is None:
                row = User(
                    id=user["id"],
                    email=normalized_email,
                    password_hash=user["password_hash"],
                    full_name=user.get("full_name"),
                    organization_id=user.get("organization_id"),
                    is_active=user.get("is_active", True),
                )
                session.add(row)
            else:
                row.password_hash = user["password_hash"]
                row.full_name = user.get("full_name")
                row.organization_id = user.get("organization_id")
                row.is_active = user.get("is_active", True)
            session.commit()
        self._store[normalized_email] = user
        return user

    def all(self) -> dict[str, dict[str, Any]]:
        self._reload_from_db()
        return dict(self._store)
