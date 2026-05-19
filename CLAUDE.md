# CLAUDE.md — Claude Code Project Context

Kurzer, handlungsleitender Kontext für Claude Code in diesem Repo.
Vollständige agentenübergreifende Regeln stehen in `AGENTS.md`.

## Projekt

Kontrollierter Microsoft-365 Executive Assistant (FastAPI-API + Power Automate).
Power Automate orchestriert dünn, die Logik liegt versioniert im Repo. MVP-Use-Case:
`EA_MorningBriefing`. Alle schreibenden Aktionen brauchen Human-in-the-loop-Freigabe.

## Kernkommandos

```bash
pip install -e ".[dev]"              # Dependencies
uvicorn ea_assistant.main:app --reload   # API lokal starten
pytest                               # Tests
ruff format --check . && ruff check .    # Format + Lint
mypy src                             # Typecheck
python scripts/validate_schemas.py   # JSON-Schemas + Beispiele prüfen
```

Vor jedem Commit: `ruff format --check .`, `ruff check .`, `pytest`,
`python scripts/validate_schemas.py` müssen grün sein.

## Arbeitsweise

1. **Analyse** — Zuerst `AGENTS.md` und relevante Specs lesen
   (`specs/`, `specs/agent-governance/`). Bestehende Funktionen/Utilities
   wiederverwenden statt neu bauen.
2. **Test zuerst** — Für Verhaltensänderungen erst Test bzw. klare Teststrategie
   (siehe Skill `test-driven-change`).
3. **Implementierung** — Kleine, klar getrennte Funktionen; Type Hints; Pydantic
   für externe Modelle. Nur spezifizierte Features bauen.
4. **Review** — Quality Gates lokal ausführen; Diff selbst prüfen.

## Guardrails

- Niemals `.env*`, Secrets, Keys oder Credentials lesen/ändern (Hook blockt dies).
- Keine verbotenen Domänen-Aktionen (`send_email`, Kalender-Mutationen, …) —
  siehe `AGENTS.md` und `specs/agent-governance/01-ai-coding-guardrails.md`.
- Keine echten personenbezogenen Daten in Tests, Logs oder Beispielen.
- Keine neuen Dependencies ohne Begründung.
- Keine destruktiven Git-Operationen ohne ausdrückliche Aufforderung.

## Skills

`.claude/skills/` enthält wiederverwendbare Workflows: `systematic-debugging`,
`test-driven-change`, `repo-maintenance`. Bei passendem Trigger anwenden.

## Weiterführend

- `AGENTS.md` — verbindliche agentenübergreifende Regeln
- `specs/AI_AGENT_BUILD_SPEC.md` — Build-Spezifikation des MVP
- `specs/agent-governance/` — Repo-Assessment, AI-Coding-Guardrails, Roadmap
- `specs/agent-governance/03-autonomous-agent-workflow.md` — autonomer
  Task-Runner (Queue, Trigger, Loop)
