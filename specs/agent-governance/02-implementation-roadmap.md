# 02 — Implementation Roadmap

Priorisierte nächste Schritte zur Härtung des Repos für AI-Coding-Agents.
Bezieht sich auf `00-repo-assessment.md`. Produkt-Roadmap des MVP: `specs/07_backlog.md`.

Priorisierung: **P0** = sofort, **P1** = als Nächstes, **P2** = später.

## P0 — sofort

- [ ] **CI aktiv halten** — `.github/workflows/ci.yml` läuft bei `pull_request`
      und `push` auf `main`. Nach erstem Lauf prüfen, dass alle Schritte grün sind.
- [ ] **mypy als echtes Gate** — `[tool.mypy]` ist in `pyproject.toml` konfiguriert;
      Dev-Stubs (`types-jsonschema`, `types-PyYAML`) ergänzt. Solange `mypy src`
      nicht dauerhaft grün ist, läuft der CI-Schritt `continue-on-error: true`.
      Ziel: Restfehler beheben, dann `continue-on-error` entfernen.
- [ ] **Branch Protection für `main`** — CI als Required Check setzen (Repo-Setting,
      manuell durch Maintainer).

## P1 — als Nächstes

- [ ] **Safety-Tests ergänzen** (NFR-004) — Tests für Prompt-Injection-Flagging und
      Sensitive-Topic-Detection auf Basis von `foundry/safety/*.jsonl`.
- [ ] **Eval-Suite in CI** — `evals/runners/run_schema_eval.py` gegen
      `evals/datasets/golden_cases.jsonl` als (zunächst non-blocking) CI-Job.
- [ ] **Coverage-Messung** — `pytest --cov` einführen, Mindestschwelle definieren.
- [ ] **Fallback-Pfad-Tests** — kontrollierte Fallback-Antwort bei Modell-/Schemafehler
      (NFR-003) testbar absichern.

## P2 — später

- [ ] **`unpack-repo-skeleton.yml` entfernen** — der Skeleton-Import ist abgeschlossen;
      der Workflow ist nicht mehr nötig (separater, bewusster Commit).
- [ ] **Dependency-/Security-Scan** — z. B. `pip-audit` als optionaler CI-Job.
- [ ] **Dead-Code-Check** — optionaler CI-Job (z. B. `ruff` Unused-Regeln /
      dediziertes Tool).
- [ ] **CONTRIBUTING.md** — Onboarding für menschliche Beitragende, verweist auf
      `AGENTS.md` und `specs/agent-governance/`.
- [ ] **Deployment-Pipeline** — Build/Deploy nach Azure Functions / Container Apps,
      sobald MVP stabil ist.

## Hinweise

- Keine neuen Laufzeit-Dependencies ohne Begründung; dev-only Type-Stubs sind ok.
- Erst MVP `EA_MorningBriefing` stabilisieren, bevor weitere Use Cases beginnen
  (siehe `AGENTS.md`, Abschnitt „Wichtig").
