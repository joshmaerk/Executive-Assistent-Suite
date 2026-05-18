# ADR-001: Keep Power Automate Thin

## Status

Accepted

## Decision

Power Automate is used for orchestration, approvals and Microsoft 365 connector actions. It must not hold prompt logic, policy logic or schema-repair logic.

## Rationale

Power Automate is difficult to version, diff and test. Prompts, policies, schemas and evaluation cases must be treated as code.

## Consequences

- Additional Assistant API component required.
- Better testability and governance.
- Easier CI/CD and regression testing.
