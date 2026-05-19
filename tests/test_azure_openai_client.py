import json
from pathlib import Path

import pytest

from ea_assistant.clients import azure_openai_client
from ea_assistant.config.settings import Settings
from ea_assistant.models.morning_briefing import (
    CriticalMeeting,
    ImportantEmail,
    MorningBriefingRequest,
    RecommendedAction,
)


def _example_request() -> MorningBriefingRequest:
    payload = json.loads(
        Path("prompts/morning_briefing/input_example.json").read_text(encoding="utf-8")
    )
    return MorningBriefingRequest.model_validate(payload)


def test_model_call_raises_when_deployment_missing(monkeypatch):
    settings = Settings(
        enable_model_calls=True,
        azure_openai_endpoint="https://example.invalid",
        azure_openai_api_key="dummy",
        azure_openai_deployment=None,
    )
    monkeypatch.setattr(azure_openai_client, "get_settings", lambda: settings)

    with pytest.raises(RuntimeError):
        azure_openai_client.call_morning_briefing_model(MorningBriefingRequest())


def test_build_mock_returns_typed_models():
    response = azure_openai_client.build_mock_morning_briefing(_example_request())

    assert response.critical_meetings
    assert all(isinstance(m, CriticalMeeting) for m in response.critical_meetings)
    assert response.important_emails
    assert all(isinstance(e, ImportantEmail) for e in response.important_emails)
    assert response.recommended_actions
    assert all(isinstance(a, RecommendedAction) for a in response.recommended_actions)
