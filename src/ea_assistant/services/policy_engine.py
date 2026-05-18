from __future__ import annotations

from pathlib import Path
import yaml

from ea_assistant.models.morning_briefing import MorningBriefingResponse, RecommendedAction


ROOT = Path(__file__).resolve().parents[3]


def load_action_policy() -> dict:
    with open(ROOT / "config/action-policy.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def contains_sensitive_topic(text: str, policy: dict | None = None) -> bool:
    policy = policy or load_action_policy()
    lowered = text.lower()
    return any(topic.lower() in lowered for topic in policy.get("sensitive_topics", []))


def contains_prompt_injection_indicator(text: str, policy: dict | None = None) -> bool:
    policy = policy or load_action_policy()
    lowered = text.lower()
    return any(indicator.lower() in lowered for indicator in policy.get("prompt_injection_indicators", []))


def enforce_action_policy(response: MorningBriefingResponse) -> MorningBriefingResponse:
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

    # Force review for sensitive content in summary-level fields.
    response_text = response.model_dump_json()
    if contains_sensitive_topic(response_text, policy):
        for meeting in response.critical_meetings:
            meeting.review_required = True
        for email in response.important_emails:
            email.review_required = True
        for risk in response.calendar_risks:
            risk.review_required = True

    return response
