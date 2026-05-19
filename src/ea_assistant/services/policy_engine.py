from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from ea_assistant.models.morning_briefing import (
    MorningBriefingRequest,
    MorningBriefingResponse,
    RecommendedAction,
)


ROOT = Path(__file__).resolve().parents[3]


def load_action_policy() -> dict:
    with open(ROOT / "config/action-policy.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def contains_sensitive_topic(text: str, policy: dict | None = None) -> bool:
    policy = policy or load_action_policy()
    lowered = text.lower()
    # Whole-word match so short topics (e.g. "hr") do not match inside
    # ordinary words (e.g. the German "durchgeführt").
    return any(
        re.search(rf"\b{re.escape(topic.lower())}\b", lowered)
        for topic in policy.get("sensitive_topics", [])
    )


def contains_prompt_injection_indicator(text: str, policy: dict | None = None) -> bool:
    policy = policy or load_action_policy()
    lowered = text.lower()
    return any(
        indicator.lower() in lowered for indicator in policy.get("prompt_injection_indicators", [])
    )


def _collect_text_values(obj: Any) -> list[str]:
    """Collect only string *values* from a nested structure, never dict keys."""
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        return [text for value in obj.values() for text in _collect_text_values(value)]
    if isinstance(obj, list):
        return [text for value in obj for text in _collect_text_values(value)]
    return []


def contains_untrusted_injection(
    request: MorningBriefingRequest, policy: dict | None = None
) -> bool:
    """Detect prompt-injection indicators in untrusted request input."""
    policy = policy or load_action_policy()
    parts: list[str] = []
    for email in request.emails:
        parts += [p for p in (email.subject, email.bodyPreview, email.bodyText) if p]
    for event in request.calendar_events:
        parts += [p for p in (event.title, event.bodyPreview) if p]
    return contains_prompt_injection_indicator(" ".join(parts), policy)


def enforce_action_policy(
    response: MorningBriefingResponse,
    request: MorningBriefingRequest | None = None,
) -> MorningBriefingResponse:
    policy = load_action_policy()
    configured_actions = policy.get("actions", {})

    sanitized_actions: list[RecommendedAction] = []
    for action in response.recommended_actions:
        cfg = configured_actions.get(action.type)
        if cfg is None or not cfg.get("allowed", False):
            sanitized_actions.append(
                RecommendedAction(
                    type="blocked",
                    target_id=action.target_id,
                    reason=action.reason,
                    requires_approval=True,
                    blocked_reason=f"Action '{action.type}' is not allowed by policy.",
                )
            )
            continue

        action.requires_approval = bool(cfg.get("requires_approval", True))
        sanitized_actions.append(action)

    response.recommended_actions = sanitized_actions

    # Force review for sensitive content or prompt injection in untrusted input.
    # Scan only content values, not the serialized structure, so field names
    # (e.g. "audit") cannot match a topic.
    content_text = " ".join(_collect_text_values(response.model_dump(mode="json")))
    force_review = contains_sensitive_topic(content_text, policy)
    if request is not None and contains_untrusted_injection(request, policy):
        force_review = True
    if force_review:
        for meeting in response.critical_meetings:
            meeting.review_required = True
        for email in response.important_emails:
            email.review_required = True
        for risk in response.calendar_risks:
            risk.review_required = True

    return response
