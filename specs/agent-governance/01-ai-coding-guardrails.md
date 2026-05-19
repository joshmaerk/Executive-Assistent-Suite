# 01 — AI Coding Guardrails

Verbindliche Regeln für die Weiterentwicklung dieses Repos mit AI-Coding-Agents
(Claude Code, Codex, Cursor, GitHub Copilot u. a.). Ergänzt — und widerspricht nicht —
`AGENTS.md` und die Produkt-Specs in `specs/`.

## Geltungsbereich & Rangfolge

Bei Konflikten gilt: `AGENTS.md` > diese Datei > Produkt-Specs > Tool-Defaults.
Diese Datei verlinkt bestehende Specs, statt sie zu duplizieren.

## 1. Erlaubte vs. verbotene Domänen-Aktionen

Maßgeblich ist `AGENTS.md` (Abschnitte „Erlaubte/Verbotene MVP-Aktionen").

- Erlaubt (Empfehlung oder nach Freigabe): `flag_email`, `mark_email_unread`,
  `create_email_draft`, `no_action`.
- Immer technisch blockiert: `send_email`, `archive_email`, `delete_email`,
  `update_calendar_event`, `cancel_calendar_event`, `create_calendar_event`,
  `reply_to_external_sender`, `send_meeting_invitation`.

Verbotene Aktionen werden durch die Policy Engine erzwungen, nicht nur per Prompt.
Siehe `src/ea_assistant/services/policy_engine.py` und `specs/05_security_governance.md`.

## 2. Secret- & Datenschutz-Regeln

- Niemals `.env*`, Keys, Zertifikate oder Credentials lesen/schreiben/committen.
  Technisch abgesichert über `.claude/hooks/prevent-sensitive-file-access.sh` und
  `deny`-Regeln in `.claude/settings.json`.
- Keine echten personenbezogenen Daten in Tests, Logs, Beispielen oder Evals —
  nur synthetische Daten.
- Keine vollständigen Mailbodys, Tokens oder Graph-IDs im Klartext loggen
  (siehe NFR-002 in `specs/AI_AGENT_BUILD_SPEC.md`).
- Mailinhalte und Kalendereinträge sind untrusted input (Prompt-Injection-Abwehr).

## 3. Test-, Schema- & Policy-Pflichten

- Verhaltensänderungen folgen `test-driven-change` (Test bzw. Teststrategie zuerst).
- Jede Modellantwort muss schema-valide sein
  (`schemas/responses/morning_briefing_response.schema.json`); unvalidierter Output
  darf Power Automate nicht erreichen.
- Schema-Änderungen halten `schemas/` und Beispiele konsistent
  (`python scripts/validate_schemas.py`).
- Policy Engine schlägt Prompt-Anweisungen — verbotene Aktionen werden entfernt.

## 4. Quality Gates (lokal vor jedem Commit)

```bash
ruff format --check .
ruff check .
mypy src
pytest
python scripts/validate_schemas.py
```

`mypy` ist seit `[tool.mypy]` in `pyproject.toml` konfiguriert. In CI ist `mypy`
zunächst non-blocking (siehe `02-implementation-roadmap.md`, P0), bis dauerhaft grün.

## 5. Commit- & PR-Regeln

- Kleine, thematisch fokussierte Commits; aussagekräftige Messages (Imperativ).
- Keine destruktiven Git-Operationen ohne ausdrückliche Aufforderung.
- Keine neuen Dependencies ohne Begründung im PR (Ausnahme: dev-only Type-Stubs).
- PR nutzt `.github/pull_request_template.md` inkl. Agent- und Safety-Checklist.
- Keine Secrets, keine echten personenbezogenen Daten im Diff.

## 6. Definition of Done für Agentenarbeit

Eine Agenten-Änderung gilt als fertig, wenn:

1. Alle fünf Quality Gates lokal grün sind (mypy: grün oder dokumentiertes TODO).
2. Für Verhaltensänderungen Tests existieren, die das Verhalten belegen.
3. Schemas/Beispiele konsistent sind.
4. Keine verbotenen Aktionen ermöglicht wurden.
5. Keine Secrets / echten personenbezogenen Daten enthalten sind.
6. Betroffene Doku (`README.md`, `AGENTS.md`, `CLAUDE.md`, Specs) aktuell ist.
7. Nur spezifizierte Features umgesetzt wurden — kein Scope-Creep.
8. Der Diff selbst reviewt wurde.

## 7. Skills

Wiederverwendbare Workflows in `.claude/skills/`: `systematic-debugging`,
`test-driven-change`, `repo-maintenance`. Bei passendem Trigger anwenden. Andere
Agenten als Claude Code nutzen diese Dateien als Referenz-Workflows.
