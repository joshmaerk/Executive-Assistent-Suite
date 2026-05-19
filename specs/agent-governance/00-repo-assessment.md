# 00 — Repo Assessment

Versionierter Snapshot des Repo-Zustands zum Zeitpunkt der Einführung der
AI-Coding-Guardrails. Stand: 2026-05-19.

## 1. Projektzweck

Kontrollierter Executive Assistant für Microsoft 365 (Outlook/Teams). Power Automate
orchestriert dünn; die Businesslogik liegt versioniert im Repo (Prompts, Schemas,
Policies, Evals, API). MVP-Use-Case: `EA_MorningBriefing`. Human-in-the-loop für alle
schreibenden Aktionen; keine autonome Außenkommunikation.

## 2. Tech Stack & Versionen

- Python `>=3.11` (lokal 3.11.x), FastAPI `>=0.110`, Uvicorn, Pydantic v2 `>=2.7`,
  pydantic-settings, jsonschema, PyYAML, `openai>=1.42`, httpx, python-dotenv.
- Dev: pytest `>=8`, pytest-asyncio, ruff `>=0.4`, mypy `>=1.9`.
- Build/Run: `pyproject.toml` (PEP 621), `Makefile`, `Dockerfile` (python:3.11-slim).
- Ziel-Deployment laut Specs: später Azure Functions / Container Apps.

## 3. Architektur- & Modulstruktur

- `src/ea_assistant/`: `main.py` (FastAPI-App), `routes/` (health, morning_briefing),
  `services/` (policy_engine, schema_validator, prompt_renderer),
  `clients/` (azure_openai_client), `models/`, `config/settings.py`.
- `prompts/`, `schemas/` (requests/responses), `config/` (dev.yaml, action-policy.yaml).
- `power-automate/`, `graph/`, `foundry/`, `evals/`, `specs/`, `docs/`.
- Codebasis klein (~440 LOC in `src`, alle Dateien < 120 Zeilen) → gut agententauglich.

## 4. Build/Run/Test/Lint/Deploy-Kommandos

| Zweck | Kommando |
|-------|----------|
| Install | `pip install -e ".[dev]"` (`make install`) |
| Run | `uvicorn ea_assistant.main:app --reload` (`make run`) |
| Test | `pytest` (`make test`) |
| Schema-Validierung | `python scripts/validate_schemas.py` (`make validate`) |
| Lint | `ruff check .` |
| Format-Check | `ruff format --check .` |
| Typecheck | `mypy src` |
| Container | `docker build -t ea-assistant .` |

## 5. Bestehende Qualitätsgates (verifiziert)

- `pytest` → 6 passed (grün).
- `ruff check .` → grün.
- `python scripts/validate_schemas.py` → grün.
- `mypy src` → zuvor 9 import-/stub-bezogene Fehler (keine `[tool.mypy]`-Konfig,
  fehlende Stubs). Mit dieser Änderung konfiguriert; siehe `01-ai-coding-guardrails.md`.

## 6. CI/CD-Struktur

- Vorher: nur `unpack-repo-skeleton.yml` (einmaliger Skeleton-Import), **keine CI**.
  Reale CI lag als Template `docs/workflows/ci.yml.template`.
- Mit dieser Änderung: aktive Pipeline `.github/workflows/ci.yml` (install, format,
  lint, schema-validate, pytest, mypy).

## 7. Testabdeckung & Testtypen

- 3 Testdateien, 6 Tests — Unit-/Kontrakt-Ebene (API, Policy-Blocking, Schema-Beispiele).
- Eval-Artefakte (`evals/`, `foundry/safety/*`) vorhanden, nicht in CI verdrahtet.
- Lücken: keine Coverage-Messung; keine Tests für Prompt-Injection-Flagging,
  Sensitive-Topic-Detection und Fallback-Pfade trotz NFR-004.

## 8. Security-/Secret-Risiken

- `.env` in `.gitignore`; `.env.example` enthält nur Platzhalter; kein Secret im Tree.
- `SECURITY.md` + `specs/05_security_governance.md` solide.
- Risiken: bisher kein technischer Schutz gegen Agent-Zugriff auf `.env*`/Keys
  (mit dieser Änderung adressiert: Hook + `deny`-Regeln); Mailinhalte = untrusted
  input, Injection-Abwehr spezifiziert aber untergetestet.

## 9. Dokumentationslücken (vor dieser Änderung)

- Kein `CLAUDE.md`; `AGENTS.md` ohne Command-Liste, Commit-/PR-Regeln, DoD-für-Agenten.
- Keine versionierte AI-Coding-Governance / Roadmap.

## 10. Risiken für AI Coding Agents

| Risiko | Status |
|--------|--------|
| Keine aktive CI | adressiert (`ci.yml`) |
| Typecheck nicht konfiguriert | adressiert (`[tool.mypy]`, CI initial non-blocking) |
| Kein Schutz sensibler Dateien | adressiert (Hook + `deny`) |
| Vermischung Produkt-Specs / Governance | adressiert (`specs/agent-governance/`) |
| Eval-Suite nicht automatisiert | offen → Roadmap P1 |
| Fehlende Injection-/Sensitive-Topic-Tests | offen → Roadmap P1 |

Positiv: kleine, klar getrennte Module; klare Konventionen in `AGENTS.md`/Specs;
schema- und policy-getriebenes Design.
