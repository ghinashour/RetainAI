from __future__ import annotations

import json
from typing import Any

import httpx

from app.core.config import get_settings


class AIAnalysisService:
    def __init__(self, settings: Any | None = None) -> None:
        self.settings = settings or get_settings()

    def analyze_portfolio(
        self,
        organization_name: str,
        customers: list[dict[str, Any]],
        metrics: dict[str, Any],
    ) -> dict[str, Any]:
        if not customers:
            return self._unavailable("no_data", "Import customer data to generate an AI analysis.")
        if not self.settings.ai_api_key:
            return self._unavailable("not_configured", "Configure AI_API_KEY to enable portfolio analysis.")

        accounts: dict[str, dict[str, Any]] = {}
        model_accounts = []
        for index, customer in enumerate(customers, start=1):
            account_ref = f"A{index}"
            accounts[account_ref] = customer
            model_accounts.append(
                {
                    "account_ref": account_ref,
                    "status": customer.get("status"),
                    "health_score": customer.get("health_score"),
                    "monthly_revenue": customer.get("monthly_revenue"),
                    "segment": customer.get("segment"),
                    "last_interaction": customer.get("last_interaction"),
                }
            )

        request_body = {
            "model": self.settings.ai_model,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a customer-retention analyst. Analyze only the supplied account and portfolio data. "
                        "Do not invent causes, history, or facts. Clearly distinguish evidence from uncertainty. "
                        "Return one JSON object with: headline (string), risk_summary (string), next_steps (array of "
                        "strings), retention_score (integer 0-100 or null when evidence is insufficient), confidence "
                        "(low, medium, or high), rationale (string), top_risk_accounts (array of {account_ref, reason}), "
                        "and recommendations (array of {account_ref, title, priority, reason, next_step}). "
                        "Only use provided account_ref values. Keep recommendations specific and actionable."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "portfolio": "Customer retention portfolio",
                            "metrics": metrics,
                            "accounts": model_accounts,
                        }
                    ),
                },
            ],
        }

        try:
            response = httpx.post(
                f"{self.settings.ai_base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {self.settings.ai_api_key}"},
                json=request_body,
                timeout=self.settings.ai_timeout_seconds,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            analysis = json.loads(content)
            return self._normalize(analysis, accounts)
        except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
            return self._unavailable("provider_error", "The AI provider could not complete the analysis.")

    @staticmethod
    def _normalize(analysis: dict[str, Any], accounts: dict[str, dict[str, Any]]) -> dict[str, Any]:
        score = analysis.get("retention_score")
        if score is not None:
            score = max(0, min(100, int(score)))

        recommendations = []
        for index, item in enumerate(analysis.get("recommendations", []), start=1):
            customer = accounts.get(item.get("account_ref"))
            if customer is None:
                continue
            recommendations.append(
                {
                    "id": f"ai-recommendation-{customer['id']}-{index}",
                    "customer_id": customer["id"],
                    "customer_name": customer["name"],
                    "title": str(item.get("title", "")),
                    "priority": item.get("priority", "Medium"),
                    "reason": str(item.get("reason", "")),
                    "next_step": str(item.get("next_step", "")),
                }
            )

        top_risk_customers = []
        for item in analysis.get("top_risk_accounts", []):
            customer = accounts.get(item.get("account_ref"))
            if customer is not None:
                top_risk_customers.append(customer["name"])

        assessment = {
            "score": score,
            "confidence": analysis.get("confidence", "low"),
            "rationale": str(analysis.get("rationale", "")),
        }
        return {
            "available": True,
            "status": "ready",
            "message": None,
            "headline": str(analysis.get("headline", "Portfolio analysis")),
            "risk_summary": str(analysis.get("risk_summary", "")),
            "next_steps": [str(step) for step in analysis.get("next_steps", [])[:5]],
            "retention_assessment": assessment,
            "top_risk_customers": top_risk_customers[:5],
            "recommendations": recommendations[:10],
        }

    @staticmethod
    def _unavailable(status: str, message: str) -> dict[str, Any]:
        return {
            "available": False,
            "status": status,
            "message": message,
            "headline": None,
            "risk_summary": None,
            "next_steps": [],
            "retention_assessment": None,
            "top_risk_customers": [],
            "recommendations": [],
        }