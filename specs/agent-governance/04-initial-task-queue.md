# 04 — Initial Task Queue

Kuratierte Startliste für die autonome Work Queue. Jeder Eintrag wird als GitHub-Issue
angelegt (Formular `.github/ISSUE_TEMPLATE/agent-task.yml`). Erst das Label
`agent-ready` (durch einen Menschen) macht eine Aufgabe für den Agenten sichtbar —
siehe `03-autonomous-agent-workflow.md`.

Reihenfolge ist MVP-/P0-first. Quelle: `02-implementation-roadmap.md` und
`specs/07_backlog.md`.

| ID | Task | Prio | Epic | `agent-ready` initial |
|----|------|------|------|------------------------|
| WQ-001 | `mypy` zum blockierenden CI-Gate machen: Reststub-Fehler beheben, `continue-on-error` in `.github/workflows/ci.yml` entfernen | P0 | governance | ja |
| WQ-002 | Tests für Prompt-Injection-Flagging auf Basis von `foundry/safety/prompt_injection_cases.jsonl` | P1 | quality | ja |
| WQ-003 | Tests für Sensitive-Topic-Detection auf Basis von `foundry/safety/sensitive_topic_cases.jsonl` | P1 | quality | ja |
| WQ-004 | Test für den kontrollierten Fallback-Pfad bei Modell-/Schemafehler (NFR-003) | P1 | quality | nein |
| WQ-005 | Coverage-Messung mit `pytest-cov` einführen und als CI-Schritt ergänzen | P1 | quality | nein |
| WQ-006 | Eval-Suite (`evals/runners/run_schema_eval.py`) als non-blocking CI-Job verdrahten | P1 | quality | nein |
| WQ-007 | Einmaligen Workflow `unpack-repo-skeleton.yml` entfernen | P2 | governance | nein |
| WQ-008 | `CONTRIBUTING.md` für menschliche Beitragende ergänzen (Verweis auf `AGENTS.md`) | P2 | governance | nein |
| WQ-009 | `pip-audit` Dependency-Scan als optionalen CI-Job ergänzen | P2 | governance | nein |
| WQ-010 | `Makefile` um Targets `format`, `lint`, `typecheck` ergänzen (Konsistenz zur CI) | P2 | governance | nein |

## Akzeptanzkriterien pro Task

Jedes erzeugte Issue beschreibt explizit: Kontext/Ziel, prüfbare Akzeptanzkriterien,
Dateien im Scope, Dinge außerhalb des Scope. Übergreifend gilt die Definition of Done
aus `01-ai-coding-guardrails.md`:

- Alle Quality Gates grün (`ruff format --check .`, `ruff check .`, `mypy src`,
  `pytest`, `python scripts/validate_schemas.py`).
- Verhaltensänderungen durch Tests belegt; Schemas/Beispiele konsistent.
- Keine Secrets, keine echten personenbezogenen Daten, keine verbotenen Aktionen.
- Keine neuen Laufzeit-Dependencies ohne Begründung (dev-only Tools wie `pytest-cov`,
  `pip-audit` sind mit Begründung im PR zulässig).

## Pflege

Abgeschlossene Tasks werden durch den Merge des zugehörigen PR (`Closes #<issue>`)
geschlossen. Neue Tasks ergänzt ein Mensch über das Issue-Formular und gibt sie bei
Bedarf mit `agent-ready` frei. Diese Datei dient als versionierte Referenz des
ursprünglichen Bootstraps und muss nicht laufend mit den Issues synchron gehalten
werden.
