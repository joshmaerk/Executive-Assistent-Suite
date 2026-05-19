import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ea_assistant.main import app
from ea_assistant.models.morning_briefing import AuditMetadata, MorningBriefingResponse
from ea_assistant.services.policy_engine import (
    contains_prompt_injection_indicator,
    enforce_action_policy,
)

client = TestClient(app)

CASES_FILE = Path("foundry/safety/prompt_injection_cases.jsonl")


def _load_cases() -> list[dict]:
    lines = CASES_FILE.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


_CASES = _load_cases()
_CASE_IDS = [case["case_id"] for case in _CASES]


@pytest.mark.parametrize("case", _CASES, ids=_CASE_IDS)
def test_indicator_detects_every_case(case):
    assert contains_prompt_injection_indicator(case["bodyText"]) is True


@pytest.mark.parametrize("case", _CASES, ids=_CASE_IDS)
def test_injection_in_email_forces_review(case):
    payload = {
        "emails": [
            {
                "id": case["case_id"],
                "sender": {"name": "External", "email": "external@example.invalid"},
                "subject": "Test",
                "receivedDateTime": "2026-05-19T08:00:00Z",
                "bodyText": case["bodyText"],
            }
        ]
    }
    response = client.post("/api/v1/morning-briefing", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert body["important_emails"]
    if case["expected"].get("review_required"):
        assert all(email["review_required"] is True for email in body["important_emails"])


def _response_with_action(action_type: str) -> MorningBriefingResponse:
    return MorningBriefingResponse(
        audit=AuditMetadata(
            request_id="test",
            model_deployment="mock",
            generated_at=datetime.now(timezone.utc).isoformat(),
        ),
        briefing_summary="Test",
        critical_meetings=[],
        calendar_risks=[],
        important_emails=[],
        decisions_expected=[],
        recommended_actions=[
            {
                "type": action_type,
                "target_id": "x",
                "reason": "injected",
                "requires_approval": True,
                "blocked_reason": None,
            }
        ],
        open_questions=[],
    )


@pytest.mark.parametrize("action_type", ["send_email", "archive_email"])
def test_injection_cannot_enable_unsafe_action(action_type):
    sanitized = enforce_action_policy(_response_with_action(action_type))
    assert sanitized.recommended_actions[0].type == "blocked"
