# Architecture

## Context Diagram

```text
User
 |
 | receives Teams Card / Mail Briefing
 v
Power Automate
 |
 | HTTP Premium
 v
Assistant API
 |
 | Azure OpenAI / Structured Output
 v
Azure AI Foundry
```

## Components

### Power Automate

- Recurrence Trigger
- Office 365 Outlook Connector
- HTTP Premium Connector
- Teams Adaptive Card / Approval
- Outlook/Graph action after approval

### Assistant API

- FastAPI service
- Prompt rendering
- Azure OpenAI client
- Schema validator
- Policy engine
- Audit metadata

### Azure OpenAI / Foundry

- Model deployment
- Evaluation dataset
- Observability
- Prompt/version management by repo
- Quality and safety evaluation

### Microsoft Graph

Used for:

- Create message draft
- Create reply draft
- Set categories
- Advanced message operations

## Key Architecture Decision

Power Automate must not contain prompt logic. Prompt logic belongs in the repo.
