# Power Automate Flow — EA_MorningBriefing

## Zweck

Erzeugt morgens ein Executive Briefing auf Basis von Outlook-Kalender und E-Mails.

## Voraussetzungen

- Power Automate
- HTTP Premium Connector
- Office 365 Outlook Connector
- Teams Connector
- Assistant API erreichbar
- Optional: Graph App / HTTP with Entra ID für Drafts

## Flow Steps

1. Trigger: Recurrence, Mo–Fr 07:15.
2. Get calendar view of events (V3) — today.
3. Get calendar view of events (V3) — tomorrow.
4. Get emails — unread/flagged since previous afternoon.
5. Compose reduced JSON payload.
6. HTTP POST to Assistant API:
   - URL: `https://<assistant-api>/api/v1/morning-briefing`
   - Method: POST
   - Headers: `Content-Type: application/json`
7. Parse JSON with schema from `schemas/responses/morning_briefing_response.schema.json`.
8. Post Adaptive Card to Teams using `power-automate/adaptive-cards/morning_briefing_card.json`.
9. Switch on user action.
10. Execute approved safe action.

## Important

Do not run write actions automatically before the Teams response.
