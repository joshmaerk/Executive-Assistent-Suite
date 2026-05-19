---
name: test-driven-change
description: Testgetriebene Umsetzung von Verhaltensänderungen im M365 Executive Assistant — erst Test bzw. klare Teststrategie, dann Implementierung. Anwenden bei neuen Features, geänderter Logik, Bugfixes mit Verhaltensänderung.
---

# Test-Driven Change

## Trigger

- Neues Feature oder neuer Endpoint.
- Geändertes Verhalten von Policy Engine, Schema Validator, Prompt Renderer oder API.
- Bugfix, der beobachtbares Verhalten ändert.

## Nicht-Trigger

- Reine Refactorings ohne Verhaltensänderung (Tests müssen unverändert grün bleiben).
- Doku-/Kommentar-/Formatierungsänderungen.
- Debugging einer unklaren Ursache (→ `systematic-debugging`).

## Workflow

1. **Spezifikation lesen** — Relevante Spec prüfen (`specs/AI_AGENT_BUILD_SPEC.md`,
   `specs/03_api_contracts.md`, `specs/05_security_governance.md`).
2. **Teststrategie** — Festlegen, welche Tests das gewünschte Verhalten belegen.
   Bestehende Tests in `tests/` als Muster nutzen
   (`test_api.py`, `test_policy_engine.py`, `test_schema_examples.py`).
3. **Test zuerst** — Fehlschlagenden Test schreiben, der das Zielverhalten beschreibt.
   Keine echten personenbezogenen Daten — synthetische Beispiele verwenden.
4. **Implementieren** — Minimale Änderung in der korrekten Schicht
   (`routes/` → `services/` → `clients/` → `models/`). Type Hints, kleine Funktionen,
   Pydantic für externe Modelle. Nur spezifizierte Features.
5. **Grün machen** — Test bestehen lassen, ohne andere Tests zu brechen.
6. **Gates** — `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`,
   `python scripts/validate_schemas.py`.
7. **Schema-Sync** — Bei Vertragsänderungen `schemas/` und Beispiele konsistent halten.

## Abbruchkriterien

- Verhalten lässt sich nicht testbar formulieren → erst Anforderung mit Mensch klären.
- Eine Änderung würde verbotene Aktionen ermöglichen (siehe `AGENTS.md`) → stoppen.

## Output

- Neue/erweiterte Tests, die das Verhalten belegen.
- Minimale, schichtgerechte Implementierung.
- Konsistente Schemas/Beispiele; alle Quality Gates grün.
