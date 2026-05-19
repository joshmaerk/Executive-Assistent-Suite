# ADR-003: AI Agent Repo Setup

## Status

Accepted

## Context

Das Repo wird mit AI-Coding-Agents (Claude Code, Codex, Cursor, GitHub Copilot)
weiterentwickelt. Probabilistische Agentenarbeit braucht expliziten Projektkontext
und deterministische Absicherung. Vor dieser Entscheidung fehlten: ein
Claude-Code-Einstiegspunkt, technischer Schutz sensibler Dateien, eine aktive
CI-Pipeline und eine versionierte AI-Coding-Governance.

## Decision

Es wird eine versionierte Spec- und Agent-Guardrail-Struktur eingeführt:

- `CLAUDE.md` als kurzer, projektspezifischer Claude-Code-Kontext; `AGENTS.md`
  bleibt agentenübergreifender Einstiegspunkt und wird um Commands, Commit-/PR-Regeln
  und eine Definition of Done für Agentenarbeit ergänzt.
- `.claude/` mit `settings.json` (sichere Default-Permissions), Hooks
  (Schutz sensibler Dateien, Auto-Format) und Skills (`systematic-debugging`,
  `test-driven-change`, `repo-maintenance`). Skills haben eine Single Source of
  Truth in `.claude/skills/`; andere Agenten referenzieren sie über `AGENTS.md`.
- `specs/agent-governance/` für Repo-Assessment, AI-Coding-Guardrails und Roadmap —
  getrennt von den bestehenden nummerierten Produkt-Specs.
- Eine aktive CI-Pipeline `.github/workflows/ci.yml` mit Format-, Lint-, Typecheck-,
  Schema- und Test-Gates.

## Rationale

- Agenten sollen Stack, Kommandos und Konventionen nicht erraten müssen.
- Verbotene Aktionen und Secret-Zugriffe müssen technisch verhindert werden, nicht
  nur per Prompt.
- Die bestehende Repo-Struktur (Produkt-Specs `00..07`, `docs/adr/`) wird respektiert;
  neue Artefakte ergänzen sie, statt sie zu überschreiben.

## Consequences

- Neue Agenten-Kontextdateien müssen mit dem Code-Stand konsistent gehalten werden
  (siehe Skill `repo-maintenance`).
- `mypy` wird als Gate eingeführt, in CI aber zunächst non-blocking, bis es dauerhaft
  grün ist (siehe `specs/agent-governance/02-implementation-roadmap.md`, P0).
- Hooks wirken nur in Claude Code; andere Agenten sind über `AGENTS.md` und CI
  abgesichert.
- Der einmalige `unpack-repo-skeleton.yml`-Workflow bleibt vorerst bestehen und wird
  als P2-Task zur Entfernung notiert.
