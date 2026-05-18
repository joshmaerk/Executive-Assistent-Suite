# MVP Scope

## In Scope

- Morning Briefing Endpoint
- JSON Schema enforced response
- Mock-mode model calls
- Policy engine
- Sensitive topic detection
- Prompt injection warning
- Teams Adaptive Card specification
- Power Automate flow blueprint

## Out of Scope

- automatic e-mail sending
- automatic calendar updates
- attachment processing
- SharePoint RAG
- multi-agent orchestration
- user preference learning
- direct tenant deployment automation

## MVP User Journey

1. Flow runs at 07:15.
2. Flow collects calendar and email summaries.
3. Flow sends payload to Assistant API.
4. API returns structured briefing.
5. Flow posts Teams card.
6. User selects actions.
7. Flow executes only approved safe actions.
