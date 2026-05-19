---
name: systematic-debugging
description: Strukturiertes Debugging für den M365 Executive Assistant — reproduzieren, Hypothesen bilden, Root Cause finden. Anwenden bei fehlschlagenden Tests, Schema-/Policy-Fehlern, falschem API-Verhalten oder unklaren Bugs.
---

# Systematic Debugging

## Trigger

- `pytest`, `ruff`, `mypy` oder `python scripts/validate_schemas.py` schlägt fehl.
- `POST /api/v1/morning-briefing` liefert falsche/ungültige Antwort.
- Schema-Validierung oder Policy Engine verhält sich unerwartet.
- Ein Bug ohne offensichtliche Ursache.

## Nicht-Trigger

- Neue Features (→ `test-driven-change`).
- Reine Aufräum-/Wartungsarbeit (→ `repo-maintenance`).
- Trivialer, offensichtlicher Einzeiler-Fix.

## Workflow

1. **Reproduzieren** — Minimalen, deterministischen Repro-Fall herstellen.
   Bevorzugt als fehlschlagender Test oder mit `prompts/morning_briefing/input_example.json`.
   `ENABLE_MODEL_CALLS=false` nutzen, um den Mock-Pfad deterministisch zu halten.
2. **Beobachten** — Genaue Fehlermeldung, Stacktrace, betroffene Datei/Zeile sammeln.
   Erst lesen, nicht raten.
3. **Hypothesen** — 1–3 konkrete, prüfbare Hypothesen zur Ursache notieren.
4. **Isolieren** — Pro Hypothese ein gezielter Check (Test, Print, Schema-Diff).
   Layer-Grenzen beachten: Route → Service → Client → Model.
5. **Root Cause** — Ursache benennen, bevor ein Fix geschrieben wird.
6. **Fix + Regressionstest** — Fix umsetzen, Test ergänzen, der den Bug abdeckt.
7. **Verifizieren** — `pytest`, `ruff check .`, `python scripts/validate_schemas.py`.

## Abbruchkriterien

- **Maximal 3 „blinde" Fix-Versuche** ohne verstandene Root Cause. Danach stoppen,
  Annahmen verwerfen, Problem neu analysieren (Phase 1–3 wiederholen).
- Wenn die Ursache außerhalb des Repos liegt (Azure OpenAI, Tenant-Config):
  dokumentieren, nicht weiter raten.

## Output

- Verstandene Root Cause (1–2 Sätze).
- Minimaler Fix in der korrekten Schicht.
- Regressionstest in `tests/`.
- Grüne Quality Gates.
