from __future__ import annotations

import csv
import io
import uuid
from typing import Any

from app.core.exceptions import ValidationError
from app.repositories.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self) -> None:
        self.repository = CustomerRepository()

    @staticmethod
    def _infer_status(health_score: int) -> str:
        if health_score < 35:
            return "Critical"
        if health_score < 60:
            return "At risk"
        return "Healthy"

    @staticmethod
    def _infer_risk(status: str) -> str:
        if status == "Critical":
            return "High"
        if status == "At risk":
            return "Medium"
        return "Low"

    @staticmethod
    def _parse_row(row: dict[str, Any]) -> dict[str, Any]:
        normalized = {str(key).strip().lower(): str(value).strip() for key, value in row.items() if key is not None}
        name = normalized.get("name") or normalized.get("customer_name")
        email = normalized.get("email")
        if not name or not email:
            raise ValidationError("Each customer row must include both name and email")

        health_score_raw = normalized.get("health_score", "100")
        try:
            health_score = int(float(health_score_raw))
        except ValueError as exc:
            raise ValidationError(f"Invalid health_score for {name}: {health_score_raw}") from exc
        health_score = max(0, min(100, health_score))

        status = normalized.get("status") or CustomerService._infer_status(health_score)
        monthly_revenue_raw = normalized.get("monthly_revenue", "0")
        try:
            monthly_revenue = float(monthly_revenue_raw)
        except ValueError as exc:
            raise ValidationError(f"Invalid monthly_revenue for {name}: {monthly_revenue_raw}") from exc

        return {
            "id": str(uuid.uuid4()),
            "name": name,
            "email": email.lower(),
            "company": normalized.get("company") or normalized.get("account") or "Unknown",
            "status": status,
            "health_score": health_score,
            "risk_level": normalized.get("risk_level") or CustomerService._infer_risk(status),
            "monthly_revenue": monthly_revenue,
            "segment": normalized.get("segment") or "Unknown",
            "last_interaction": normalized.get("last_interaction") or "N/A",
        }

    def list_customers(self, organization_id: str | None) -> list[dict[str, Any]]:
        if not organization_id:
            return []

        customers = self.repository.list_for_organization(organization_id)
        return customers

    def import_customers(
        self,
        organization_id: str,
        csv_text: str | None = None,
        customer_rows: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        if not organization_id:
            raise ValidationError("Customer import requires an authenticated organization")

        input_rows: list[dict[str, Any]] = []
        if csv_text:
            reader = csv.DictReader(io.StringIO(csv_text))
            input_rows = list(reader)
        elif customer_rows:
            input_rows = customer_rows
        else:
            raise ValidationError("CSV content or customer rows are required for import")

        if not input_rows:
            raise ValidationError("No customer data was provided for import")

        imported: list[dict[str, Any]] = []
        for row in input_rows:
            parsed = self._parse_row(row)
            existing = self.repository.get_by_email(organization_id, parsed["email"])
            payload = {
                **parsed,
                "organization_id": organization_id,
                "id": existing["id"] if existing else parsed["id"],
            }
            self.repository.upsert(payload)
            imported.append({
                "id": payload["id"],
                "name": payload["name"],
                "email": payload["email"],
                "company": payload.get("company"),
                "status": payload.get("status"),
                "health_score": payload.get("health_score"),
                "risk_level": payload.get("risk_level"),
                "monthly_revenue": payload.get("monthly_revenue"),
                "segment": payload.get("segment"),
                "last_interaction": payload.get("last_interaction"),
            })

        return imported
