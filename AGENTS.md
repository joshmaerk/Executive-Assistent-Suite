# AGENTS.md — Build Instructions for AI Coding Agents

## Rolle des Coding Agents

Du bist ein Senior AI Engineering Agent. Baue einen produktionsnahen, aber MVP-fähigen Microsoft-365 Executive Assistant.

Du arbeitest in diesem Repository. Halte dich strikt an diese Reihenfolge:

1. Lies `specs/AI_AGENT_BUILD_SPEC.md`.
2. Lies `specs/00_product_brief.md`.
3. Lies `specs/01_architecture.md`.
4. Lies `specs/03_api_contracts.md`.
5. Implementiere zuerst ausschließlich `EA_MorningBriefing`.
6. Schreibe Tests vor oder parallel zur Implementierung.
7. Führe Schema-, Policy- und Sicherheitsprüfungen aus.
8. Keine nicht spezifizierten Features bauen.

## Grundsätze

- Power Automate orchestriert nur.
- Die Assistant API enthält die Logik.
- Prompts, JSON-Schemas, Policies und Evals sind versionierte Artefakte.
- Alle schreibenden Aktionen erfordern Freigabe.
- Modellantworten müssen schema-valide sein.
- Policy Engine schlägt Prompt-Anweisungen.
- Verbotene Aktionen werden technisch blockiert, nicht nur per Prompt verboten.

## Erlaubte MVP-Aktionen

Nur als Empfehlung oder nach expliziter Freigabe:

- `flag_email`
- `mark_email_unread`
- `create_email_draft`
- `no_action`

## Verbotene MVP-Aktionen

Immer blockieren:

- `send_email`
- `archive_email`
- `delete_email`
- `update_calendar_event`
- `cancel_calendar_event`
- `create_calendar_event`
- `reply_to_external_sender`
- `send_meeting_invitation`

## Technischer Zielstack

- Python 3.11+
- FastAPI
- Pydantic v2
- Azure OpenAI via OpenAI Python SDK oder HTTP-kompatibler Client
- JSON Schema Validation
- pytest
- GitHub Actions CI
- Optional später: Azure Functions oder Azure Container Apps

## Definition of Done für MVP

Der MVP ist fertig, wenn:

1. `POST /api/v1/morning-briefing` lauffähig ist.
2. Input gegen Pydantic-Modelle validiert wird.
3. Prompt aus `prompts/morning_briefing/prompt.md` gerendert wird.
4. Azure OpenAI mit Structured Outputs oder JSON-Schema-konformer Antwort aufgerufen wird.
5. Antwort gegen `schemas/responses/morning_briefing_response.schema.json` validiert wird.
6. Policy Engine verbotene Aktionen entfernt/blockiert.
7. Tests für Policy Engine, Schema und API-Kontrakt bestehen.
8. Beispielinput aus `prompts/morning_briefing/input_example.json` erfolgreich verarbeitet wird.
9. CI läuft grün.
10. Keine echten personenbezogenen Daten in Tests, Logs oder Beispielen enthalten sind.

## Security Requirements

- Keine Secrets committen.
- `.env` wird ignoriert.
- Key Vault / Managed Identity für produktiven Betrieb verwenden.
- Payloads in Logs redigieren.
- Keine vollständigen Mailbodys in Application Insights loggen.
- Prompt-Injection durch E-Mail-Inhalte als untrusted input behandeln.

## Code Style

- Schreibe klare, kleine Funktionen.
- Nutze Type Hints.
- Nutze Pydantic für externe API-Modelle.
- Trenne Clients, Services, Models und Policies.
- Fehler robust behandeln.
- Keine pauschalen `except Exception: pass`.
- Keine Annahmen über Tenant-spezifische IDs.

## Commands

```bash
pip install -e ".[dev]"                  # Install (oder: make install)
uvicorn ea_assistant.main:app --reload   # API lokal (oder: make run)
pytest                                   # Tests (oder: make test)
ruff format --check . && ruff check .    # Format-Check + Lint
mypy src                                 # Typecheck
python scripts/validate_schemas.py       # Schemas + Beispiele (oder: make validate)
```

Vor jedem Commit müssen `ruff format --check .`, `ruff check .`, `pytest` und
`python scripts/validate_schemas.py` grün sein.

## Commit- & PR-Regeln

- Kleine, thematisch fokussierte Commits; Messages im Imperativ.
- Keine destruktiven Git-Operationen ohne ausdrückliche Aufforderung.
- Keine neuen Dependencies ohne Begründung im PR (Ausnahme: dev-only Type-Stubs).
- PRs nutzen `.github/pull_request_template.md` inkl. Agent- und Safety-Checklist.
- Keine Secrets und keine echten personenbezogenen Daten im Diff.

## Definition of Done für Agentenarbeit

1. Alle Quality Gates lokal grün (`mypy`: grün oder dokumentiertes TODO).
2. Für Verhaltensänderungen existieren belegende Tests.
3. Schemas und Beispiele sind konsistent.
4. Keine verbotenen Aktionen ermöglicht; keine Secrets / echten Personendaten.
5. Betroffene Doku (`README.md`, `CLAUDE.md`, Specs) ist aktuell.
6. Nur spezifizierte Features umgesetzt; Diff selbst reviewt.

## Autonomer Agenten-Workflow

Aufgaben werden als GitHub Issues geführt. Ein autonomer Task-Runner zieht das
oberste mit `agent-ready` freigegebene Issue, plant, implementiert test-first,
prüft die Quality Gates und öffnet einen Pull Request — ein Mensch merged.
Verbindliche Loop-Logik: `specs/agent-governance/03-autonomous-agent-workflow.md`.

## Weiterführend

- `CLAUDE.md` — projektspezifischer Claude-Code-Kontext.
- `.claude/skills/` — Workflows `systematic-debugging`, `test-driven-change`,
  `repo-maintenance` (auch für Codex/Cursor/Copilot als Referenz nutzbar).
- `specs/agent-governance/` — Repo-Assessment, AI-Coding-Guardrails, autonomer
  Workflow, Task-Queue, Roadmap.

## Wichtig

Baue kein Agenten-Framework, bevor der Morning-Briefing-MVP stabil ist. Erst stabiler API-MVP, dann weitere Use Cases.
