import json
from types import SimpleNamespace
from unittest.mock import Mock

import httpx

from app.services.ai_analysis_service import AIAnalysisService


def test_ai_analysis_anonymizes_accounts_and_maps_recommendations(monkeypatch) -> None:
    provider_result = {
        "headline": "Renewal risk is concentrated in one account.",
        "risk_summary": "The lowest health score belongs to A1.",
        "next_steps": ["Review the account's recent usage."],
        "retention_score": 62,
        "confidence": "medium",
        "rationale": "The account has a low health score.",
        "top_risk_accounts": [{"account_ref": "A1", "reason": "Low health score"}],
        "recommendations": [
            {
                "account_ref": "A1",
                "title": "Review renewal risk",
                "priority": "High",
                "reason": "Health score is low.",
                "next_step": "Contact the account owner.",
            }
        ],
    }
    post = Mock(
        return_value=httpx.Response(
            200,
            json={"choices": [{"message": {"content": json.dumps(provider_result)}}]},
            request=httpx.Request("POST", "https://ai.example/v1/chat/completions"),
        )
    )
    monkeypatch.setattr("app.services.ai_analysis_service.httpx.post", post)
    service = AIAnalysisService(
        SimpleNamespace(
            ai_api_key="test-key",
            ai_base_url="https://ai.example/v1",
            ai_model="test-model",
            ai_timeout_seconds=5,
        )
    )

    result = service.analyze_portfolio(
        "Private organization name",
        [{
            "id": "customer-1",
            "name": "Private Customer",
            "email": "private@example.com",
            "status": "At risk",
            "health_score": 42,
            "monthly_revenue": 12000,
            "segment": "Enterprise",
            "last_interaction": "2 days ago",
        }],
        {"total_customers": 1},
    )

    sent_text = json.dumps(post.call_args.kwargs["json"])
    assert "private@example.com" not in sent_text
    assert "Private Customer" not in sent_text
    assert "Private organization name" not in sent_text
    assert '"account_ref": "A1"' in sent_text
    assert result["available"] is True
    assert result["recommendations"][0]["customer_id"] == "customer-1"
    assert result["top_risk_customers"] == ["Private Customer"]


def test_ai_analysis_reports_missing_provider_configuration() -> None:
    service = AIAnalysisService(SimpleNamespace(ai_api_key=None))

    result = service.analyze_portfolio("Workspace", [{"id": "customer-1"}], {})

    assert result["available"] is False
    assert result["status"] == "not_configured"
    assert result["recommendations"] == []