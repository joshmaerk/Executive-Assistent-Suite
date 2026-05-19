# 03 — Autonomous Agent Workflow

Operating Manual für den autonomen AI-Coding-Agenten. Dies ist die **Single Source
of Truth** für die Loop-Logik; die Trigger-Workflows (`.github/workflows/agent-*.yml`)
verweisen nur kurz hierauf.

Verbindlich gelten zusätzlich `AGENTS.md`, `CLAUDE.md` und
`specs/agent-governance/01-ai-coding-guardrails.md`.

## Prinzip

- **Ein Lauf = ein Issue.** „Nächstes nehmen" entsteht dadurch, dass der nächste
  geplante Lauf erneut das oberste freigegebene Issue zieht.
- **Mensch steuert das *Was*** (gibt Issues per Label `agent-ready` frei und merged
  PRs). **Agent macht das *Wie*** (plant, implementiert, testet, bessert nach).
- Der Agent pusht nie nach `main` und merged nie selbst.

## Work Queue: GitHub Issues + Labels

| Label | Bedeutung |
|-------|-----------|
| `agent-ready` | Issue ist spezifiziert und freigegeben; ein Agent darf es übernehmen |
| `agent-in-progress` | Aktuell von einem Agenten in Bearbeitung (Doppelvergabe-Schutz) |
| `agent-blocked` | Agent hat abgebrochen; braucht menschliche Klärung |
| `priority:P0` / `priority:P1` / `priority:P2` | Priorität (P0 = sofort) |
| `epic:morning-briefing` / `epic:governance` / `epic:quality` | Themenzuordnung |

Neue Aufgaben werden über das Issue-Formular `.github/ISSUE_TEMPLATE/agent-task.yml`
angelegt. Erst wenn ein Mensch `agent-ready` setzt, ist die Aufgabe für den Agenten
sichtbar.

## Rolle `pick-next`

Ausgelöst durch `agent-pick-next.yml` (Cron, manuell, oder neues `agent-ready`-Label).

1. **Select** — Offene Issues mit Label `agent-ready` **und ohne** `agent-in-progress`
   listen. Sortierung: `priority:P0` > `P1` > `P2`, bei Gleichstand ältestes zuerst.
   Gibt es keins → sauber und kommentarlos beenden.
2. **Claim** — Oberstes Issue wählen. Label `agent-in-progress` setzen. Kurzen
   Start-Kommentar posten (Issue-Nummer, Branch-Name).
3. **Plan** — `AGENTS.md`, `CLAUDE.md`, die im Issue referenzierten Specs und den
   Issue-Text lesen. Einen knappen Umsetzungsplan als Issue-Kommentar posten.
4. **Branch** — `agent/<issue-nummer>-<kurz-slug>` von aktuellem `main` erstellen.
5. **Implement** — Test-first nach Skill `.claude/skills/test-driven-change`.
   Kleine, schichtgerechte Änderungen; nur den Issue-Scope; keine neuen Dependencies
   ohne Begründung.
6. **Test** — Alle Quality Gates lokal grün machen:
   ```bash
   ruff format --check .
   ruff check .
   mypy src
   pytest
   python scripts/validate_schemas.py
   ```
7. **PR** — Pull Request gegen `main` öffnen, `.github/pull_request_template.md`
   ausfüllen (inkl. Agent- und Safety-Checklist), Beschreibung mit `Closes #<issue>`.
8. **Stop** — Lauf beenden. **Kein Merge.** Ein Mensch reviewt und merged.

## Rolle `iterate`

Ausgelöst durch `agent-pr-fix.yml` bei fehlgeschlagener CI oder einem Review-Kommentar
auf einem `agent/*`-PR.

1. Auslöser bestimmen: CI-Fehler-Log **oder** Review-/Kommentartext lesen.
2. Root Cause nach Skill `.claude/skills/systematic-debugging` ermitteln.
3. Minimalen Fix auf **denselben** `agent/*`-Branch pushen.
4. Quality Gates lokal erneut grün machen.
5. PR-Checkliste aktualisieren; bei Bedarf knapp im PR kommentieren.
6. **Kein Merge.**

## Abbruchkriterien

Bei einem der folgenden Punkte: Label `agent-blocked` setzen, `agent-in-progress`
entfernen, präzisen Kommentar mit dem Grund posten, Lauf beenden.

- Anforderung im Issue ist mehrdeutig oder unvollständig.
- Die Lösung erfordert Scope-Creep über den Issue-Scope hinaus.
- Quality Gates sind nach 3 ernsthaften, analysierten Versuchen weiterhin rot.
- Eine verbotene Domänen-Aktion (siehe `AGENTS.md`) wäre nötig.
- Eine Secret-/Berechtigungsgrenze wird erreicht.

## Sicherheits- & Kostenregeln

- Nie nach `main` pushen, nie selbst mergen, nur ein Issue pro Lauf.
- `concurrency`-Gruppe im Workflow verhindert Parallelläufe; `agent-in-progress`
  verhindert Doppelvergabe.
- `--max-turns` und `timeout-minutes` deckeln Laufzeit und Kosten.
- Es gelten die `deny`-Regeln und Hooks aus `.claude/settings.json` sowie alle
  Guardrails aus `01-ai-coding-guardrails.md`.

## Setup (einmalig, durch einen Menschen mit Repo-Admin-Rechten)

Ohne diese Schritte existieren die Workflow-Dateien zwar, laufen aber nicht.

1. **GitHub-App** — Anthropic-`claude`-App
   (https://github.com/apps/claude) oder eine eigene App mit den Repo-Rechten
   Contents / Issues / Pull requests (jeweils Read & Write) installieren. Bei
   eigener App: Secrets `APP_ID` und `APP_PRIVATE_KEY` setzen.
2. **Azure / Microsoft Foundry** — Foundry-Resource mit Claude-Deployment anlegen.
   GitHub-OIDC ↔ Azure als Federated Credential einrichten. Repo-Secrets:
   `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`. Repo-Variable:
   `ANTHROPIC_FOUNDRY_BASE_URL` (z. B. `https://<resource>.services.ai.azure.com`).
   Modell-Deployment-Name im Workflow unter `--model` eintragen.
3. **Branch Protection** für `main` — `ci` als Required Check, Review erforderlich.
   Stellt die „Mensch merged"-Grenze technisch sicher.
4. **Actions freigeben** — unter Settings → Actions sicherstellen, dass Workflows
   laufen dürfen.

Die exakten Action-Inputs (`use_foundry`, `ANTHROPIC_FOUNDRY_BASE_URL`) gegen die
gepinnte Version von `anthropics/claude-code-action` prüfen — siehe TODO-Kommentare
in den Workflow-Dateien.

## Queue bootstrappen

Die kuratierte Startliste steht in `04-initial-task-queue.md`. Daraus werden
GitHub-Issues erstellt; ein Mensch gibt sie durch Setzen von `agent-ready` frei.
