# ADR-002: Structured Output by JSON Schema

## Status

Accepted

## Decision

All model outputs must be structured and schema-validated.

## Rationale

Power Automate requires reliable machine-readable outputs. Free-text model outputs are unsuitable for workflow branching.

## Consequences

- Each use case requires a JSON schema.
- CI validates schemas.
- Runtime rejects invalid responses.
