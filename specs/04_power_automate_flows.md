# Power Automate Flow Specification

## Flow: EA_MorningBriefing

### Trigger

- Recurrence
- Monday to Friday
- Suggested time: 07:15 Europe/Vienna

### Steps

1. Initialize variables:
   - `sinceTimestamp`
   - `todayStart`
   - `todayEnd`
   - `tomorrowStart`
   - `tomorrowEnd`
2. Office 365 Outlook: Get calendar view of events for today.
3. Office 365 Outlook: Get calendar view of events for tomorrow.
4. Office 365 Outlook: Get emails matching unread or flagged since timestamp.
5. Select / Compose: reduce payload.
6. HTTP Premium: POST to Assistant API `/api/v1/morning-briefing`.
7. Parse JSON with response schema.
8. Post Adaptive Card to Teams.
9. Wait for response.
10. Switch on approved action:
    - flag email
    - mark unread
    - create draft through Graph
    - no action

### Payload Reduction

Do not send full raw mailbox exports. For each email include:

- id
- sender
- subject
- receivedDateTime
- importance
- bodyPreview
- max 2,000 chars sanitized body text
- hasAttachments
- categories
- isRead
- flag status

### Failure Behavior

If API fails:

- post fallback Teams message
- do not execute actions
- include request ID
