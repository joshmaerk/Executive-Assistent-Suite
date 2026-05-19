---
name: repo-maintenance
description: Wartung des M365-Executive-Assistant-Repos — Abhängigkeiten, Dead Code, Struktur, Dokumentation und CI gesund halten. Anwenden bei Aufräumarbeiten, Dependency-Updates, Konsistenzprüfungen.
---

# Repo Maintenance

## Trigger

- Geplante Aufräum-/Wartungsarbeit.
- Dependency-Update oder -Prüfung.
- Doku/Specs sind nicht mehr konsistent mit dem Code.
- CI-Pflege oder Quality-Gate-Anpassung.

## Nicht-Trigger

- Neue Features (→ `test-driven-change`).
- Aktive Bug-Suche (→ `systematic-debugging`).
- Breite Refactorings ohne klaren Auftrag.

## Workflow

1. **Bestandsaufnahme** — `git status` prüfen; aktuelle Quality Gates ausführen:
   `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`,
   `python scripts/validate_schemas.py`.
2. **Dependencies** — `pyproject.toml` prüfen. Neue Dependencies nur mit Begründung;
   bevorzugt vorhandene Bibliotheken wiederverwenden. Versions-Constraints konsistent.
3. **Dead Code / Struktur** — Ungenutzte Module, Importe, tote Pfade identifizieren.
   Schichtentrennung wahren (`routes/`, `services/`, `clients/`, `models/`, `config/`).
4. **Dokumentation** — `README.md`, `AGENTS.md`, `CLAUDE.md`, `specs/` und
   `specs/agent-governance/` gegen den realen Code-Stand abgleichen. Tote Links
   und veraltete Kommandos korrigieren.
5. **CI** — `.github/workflows/ci.yml` gegen die tatsächlichen Repo-Kommandos prüfen.
   Nur real vorhandene Kommandos; Lücken als TODO markieren statt zu raten.
6. **Verifizieren** — Alle Gates erneut grün; Diff selbst reviewen.

## Abbruchkriterien

- Eine Änderung würde Fachlogik oder öffentliche API-Kontrakte ändern → stoppen,
  als separaten `test-driven-change` behandeln.
- Unsicherheit über Stack/Command → als TODO/Assumption dokumentieren, nicht raten.
- Destruktive Git-Operationen → nur nach ausdrücklicher Aufforderung.

## Output

- Kleiner, klar abgegrenzter Wartungs-Diff.
- Aktualisierte Dokumentation/CI passend zum Code-Stand.
- Alle Quality Gates grün; Annahmen explizit notiert.
