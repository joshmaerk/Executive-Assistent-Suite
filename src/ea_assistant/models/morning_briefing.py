from typing import Literal
from pydantic import BaseModel, Field
from ea_assistant.models.domain_models import CalendarEvent, EmailItem, PolicyConfig, UserContext


class MorningBriefingRequest(BaseModel):
    request_id: str | None = None
    user_context: UserContext = Field(default_factory=UserContext)
    calendar_events: list[CalendarEvent] = []
    emails: list[EmailItem] = []
    policy: PolicyConfig = Field(default_factory=PolicyConfig)


class CriticalMeeting(BaseModel):
    event_id: str
    title: str
    start: str
    end: str
    priority: Literal["high", "medium", "low"]
    reason: str
    preparation_needed: bool
    recommended_preparation: str
    review_required: bool


class CalendarRisk(BaseModel):
    risk_type: Literal["conflict", "no_buffer", "missing_agenda", "overload", "unclear"]
    description: str
    affected_event_ids: list[str]
    suggested_action: str
    review_required: bool


class ImportantEmail(BaseModel):
    message_id: str
    sender: str
    subject: str
    summary: str
    priority: Literal["high", "medium", "low"]
    recommended_marker: Literal["flag", "leave_unread", "no_marker", "review_manually"]
    reason: str
    draft_reply_needed: bool
    draft_reply: str
    review_required: bool


class DecisionExpected(BaseModel):
    topic: str
    source: str
    decision_needed: str
    deadline: str | None = None
    uncertainty: str


class RecommendedAction(BaseModel):
    # Intentionally not a Literal: model output may propose unsafe actions.
    # The Policy Engine must sanitize to allowed response-schema values before returning.
    type: str
    target_id: str | None = None
    reason: str
    requires_approval: bool
    blocked_reason: str | None = None


class AuditMetadata(BaseModel):
    request_id: str
    use_case: str = "EA_MorningBriefing"
    prompt_version: str = "morning_briefing.v0.1.0"
    schema_version: str = "morning_briefing_response.v0.1.0"
    policy_version: str = "action_policy.v0.1.0"
    model_deployment: str | None = None
    generated_at: str


class MorningBriefingResponse(BaseModel):
    audit: AuditMetadata
    briefing_summary: str
    critical_meetings: list[CriticalMeeting]
    calendar_risks: list[CalendarRisk]
    important_emails: list[ImportantEmail]
    decisions_expected: list[DecisionExpected]
    recommended_actions: list[RecommendedAction]
    open_questions: list[str]
