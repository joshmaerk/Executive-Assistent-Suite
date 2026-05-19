from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from ea_assistant.config.settings import get_settings
from ea_assistant.models.morning_briefing import (
    AuditMetadata,
    MorningBriefingRequest,
    MorningBriefingResponse,
)
from ea_assistant.services.prompt_renderer import render_morning_briefing_prompt

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


def build_mock_morning_briefing(payload: MorningBriefingRequest) -> MorningBriefingResponse:
    request_id = payload.request_id or str(uuid4())
    now = datetime.now(timezone.utc).isoformat()

    critical_meetings = []
    if payload.calendar_events:
        event = payload.calendar_events[0]
        critical_meetings.append(
            {
                "event_id": event.id,
                "title": event.title,
                "start": event.start,
                "end": event.end,
                "priority": "medium",
                "reason": "Erster Termin im Beispielinput; im Mock-Modus keine echte KI-Bewertung.",
                "preparation_needed": True,
                "recommended_preparation": "Agenda prüfen und offene Entscheidungen klären.",
                "review_required": False,
            }
        )

    important_emails = []
    if payload.emails:
        email = payload.emails[0]
        important_emails.append(
            {
                "message_id": email.id,
                "sender": email.sender.email or email.sender.name or "unknown",
                "subject": email.subject,
                "summary": "Mock-Zusammenfassung der wichtigsten E-Mail.",
                "priority": "medium",
                "recommended_marker": "flag",
                "reason": "E-Mail wurde im Beispielinput übergeben.",
                "draft_reply_needed": False,
                "draft_reply": "",
                "review_required": False,
            }
        )

    return MorningBriefingResponse(
        audit=AuditMetadata(
            request_id=request_id,
            model_deployment=get_settings().azure_openai_deployment,
            generated_at=now,
        ),
        briefing_summary="Mock-Briefing: Bitte ENABLE_MODEL_CALLS=true setzen, um Azure OpenAI zu verwenden.",
        critical_meetings=critical_meetings,
        calendar_risks=[],
        important_emails=important_emails,
        decisions_expected=[],
        recommended_actions=[
            {
                "type": "flag_email",
                "target_id": payload.emails[0].id if payload.emails else None,
                "reason": "Flag-Vorschlag aus Mock-Modus.",
                "requires_approval": True,
                "blocked_reason": None,
            }
        ]
        if payload.emails
        else [],
        open_questions=["Mock-Modus aktiv; keine echte Modellanalyse durchgeführt."],
    )


def call_morning_briefing_model(payload: MorningBriefingRequest) -> MorningBriefingResponse:
    settings = get_settings()

    if not settings.enable_model_calls:
        return build_mock_morning_briefing(payload)

    if OpenAI is None:
        raise RuntimeError("openai package is not installed")

    if not settings.azure_openai_endpoint or not settings.azure_openai_api_key:
        raise RuntimeError("Azure OpenAI endpoint/key missing")

    messages = render_morning_briefing_prompt(payload)

    # Note:
    # The exact structured output call can be implemented via response_format=json_schema.
    # This stub intentionally keeps the implementation thin until tenant-specific model deployment
    # and API version are confirmed.
    client = OpenAI(
        base_url=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
    )

    completion = client.chat.completions.create(
        model=settings.azure_openai_deployment,
        messages=messages,
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    raw = completion.choices[0].message.content
    if raw is None:
        raise RuntimeError("Azure OpenAI returned empty content")

    return MorningBriefingResponse.model_validate_json(raw)
