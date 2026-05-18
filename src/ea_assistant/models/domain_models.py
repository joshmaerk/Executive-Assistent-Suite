from pydantic import BaseModel, Field


class Person(BaseModel):
    name: str | None = None
    email: str | None = None


class EmailItem(BaseModel):
    id: str = Field(..., description="M365 message id or stable flow-local id.")
    sender: Person
    subject: str
    receivedDateTime: str
    importance: str | None = None
    bodyPreview: str | None = None
    bodyText: str | None = None
    hasAttachments: bool = False
    categories: list[str] = []
    isRead: bool | None = None
    flagStatus: str | None = None


class CalendarEvent(BaseModel):
    id: str
    title: str
    start: str
    end: str
    organizer: Person | None = None
    attendees: list[Person] = []
    location: str | None = None
    bodyPreview: str | None = None
    isOnlineMeeting: bool | None = None
    importance: str | None = None
    sensitivity: str | None = None


class UserContext(BaseModel):
    role: str = "bereichsleiter"
    timezone: str = "Europe/Vienna"
    language: str = "de"
    briefing_date: str | None = None


class PolicyConfig(BaseModel):
    allow_send_email: bool = False
    allow_update_calendar: bool = False
    allow_archive_email: bool = False
    allow_create_draft: bool = True
    allow_flag_email: bool = True
