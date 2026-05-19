# Setup-Handbuch — Projekt in einer GitHub-Instanz scharf schalten

Diese Anleitung führt dich Schritt für Schritt durch alles, was du **einmalig** in
deinem GitHub tun musst, um aus diesem Repo eine lauffähige Entwicklungsumgebung mit
autonomem AI-Coding-Workflow zu machen.

Reihenfolge einhalten — spätere Schritte setzen frühere voraus.
Legende: 🤖 läuft automatisch · 🧑 manueller Schritt durch dich.

---

## Schritt 0 — Repo in dein GitHub bringen

🧑 Repo anlegen und Code übertragen:

```bash
# Variante A: vorhandenes lokales Repo auf dein neues Remote pushen
git remote set-url origin https://github.com/<dein-account>/<dein-repo>.git
git push -u origin --all
git push -u origin --tags
```

Danach: prüfe, dass `main` und der Arbeitsbranch im neuen Repo sichtbar sind.

> Wichtig: Die Links in `.github/ISSUE_TEMPLATE/config.yml` zeigen auf
> `joshmaerk/Executive-Assistent-Suite`. Passe sie auf `<dein-account>/<dein-repo>`
> an, sonst verweisen die Issue-Hilfelinks ins alte Repo.

---

## Schritt 1 — Lokale Entwicklungsumgebung

🧑 Einmalig lokal einrichten und prüfen, dass alles grün ist:

```bash
git clone https://github.com/<dein-account>/<dein-repo>.git
cd <dein-repo>

python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

cp .env.example .env                 # echte Werte NICHT committen

chmod +x .claude/hooks/*.sh          # Hooks ausführbar machen (Linux/macOS)
```

Quality Gates lokal verifizieren — alle müssen grün sein:

```bash
ruff format --check .
ruff check .
mypy src
pytest
python scripts/validate_schemas.py
```

API lokal starten (optional):

```bash
uvicorn ea_assistant.main:app --reload
```

---

## Schritt 2 — CI aktivieren

🤖 `.github/workflows/ci.yml` läuft **automatisch** bei jedem Push auf `main` und bei
jedem Pull Request. Nach dem ersten Push: unter **Actions** prüfen, dass der Workflow
`ci` grün durchläuft.

🧑 **Branch Protection für `main`** einrichten (Pflicht für den autonomen Workflow):

GitHub → **Settings → Branches → Add branch ruleset** (oder *Branch protection rule*)
für `main`:

- ✅ Require a pull request before merging
- ✅ Require status checks to pass → Check `ci` auswählen
- ✅ Require approvals (mindestens 1)

Damit ist technisch garantiert: niemand — auch kein Agent — schreibt direkt auf
`main`; jede Änderung läuft über einen geprüften PR.

---

## Schritt 3 — Zugänge für den autonomen Agenten

Der autonome Workflow nutzt `anthropics/claude-code-action` mit Azure / Microsoft
Foundry. Dafür sind drei Dinge nötig.

### 3a 🧑 GitHub-App installieren

Entweder die offizielle Anthropic-App (https://github.com/apps/claude) auf dein Repo
installieren, **oder** eine eigene GitHub-App anlegen
(https://github.com/settings/apps/new) mit den Repo-Rechten:

- Contents: Read & write
- Issues: Read & write
- Pull requests: Read & write
- Webhooks: deaktiviert

Bei eigener App: Private Key (`.pem`) erzeugen und als Repo-Secrets hinterlegen:

- `APP_ID` — die App-ID
- `APP_PRIVATE_KEY` — Inhalt der `.pem`-Datei

### 3b 🧑 Azure / Microsoft Foundry einrichten

1. In Azure eine **Foundry-Resource** mit einem **Claude-Modell-Deployment** anlegen.
2. **GitHub-OIDC ↔ Azure** verbinden: in der Azure-App-Registration einen
   *Federated Credential* für GitHub Actions anlegen (Issuer
   `https://token.actions.githubusercontent.com`, Subject auf dein Repo/Branch).
3. Repo-Secrets setzen (**Settings → Secrets and variables → Actions → Secrets**):
   - `AZURE_CLIENT_ID`
   - `AZURE_TENANT_ID`
   - `AZURE_SUBSCRIPTION_ID`
4. Repo-Variable setzen (**… → Variables**):
   - `ANTHROPIC_FOUNDRY_BASE_URL` — z. B. `https://<resource>.services.ai.azure.com`

### 3c 🧑 Modellnamen in den Workflows eintragen

In `.github/workflows/agent-pick-next.yml` und `agent-pr-fix.yml` den Platzhalter
`--model claude-sonnet-4-5` durch den **Namen deines Foundry-Deployments** ersetzen.

> Prüfe die exakten Action-Inputs (`use_foundry`, `ANTHROPIC_FOUNDRY_BASE_URL`) gegen
> die Doku der von dir genutzten `claude-code-action`-Version — sie können sich
> zwischen Versionen ändern (siehe TODO-Kommentare in den Workflow-Dateien).

---

## Schritt 4 — Work Queue anlegen (Labels + Issues)

Die Aufgaben des Agenten leben als GitHub Issues. Logik dahinter:
`specs/agent-governance/03-autonomous-agent-workflow.md`.

### 4a 🧑 Labels anlegen

Per UI (**Issues → Labels → New label**) oder mit der GitHub-CLI:

```bash
gh label create "agent-ready"          -c "0e8a16" -d "Freigegeben, Agent darf uebernehmen"
gh label create "agent-in-progress"    -c "fbca04" -d "Agent arbeitet daran"
gh label create "agent-blocked"        -c "d93f0b" -d "Abgebrochen, braucht Mensch"
gh label create "priority:P0"          -c "b60205" -d "Sofort"
gh label create "priority:P1"          -c "d93f0b" -d "Als Naechstes"
gh label create "priority:P2"          -c "fbca04" -d "Spaeter"
gh label create "epic:morning-briefing" -c "1d76db" -d "Use Case Morning Briefing"
gh label create "epic:governance"      -c "5319e7" -d "Repo-/Prozess-Haertung"
gh label create "epic:quality"         -c "006b75" -d "Tests, Coverage, Evals"
```

### 4b 🧑 Seed-Issues anlegen

Die kuratierte Startliste steht in `specs/agent-governance/04-initial-task-queue.md`
(WQ-001 bis WQ-010). Lege pro Eintrag ein Issue an — entweder über das Formular
**Issues → New issue → „Agent Task"** oder per CLI, z. B.:

```bash
gh issue create \
  --title "[Task] WQ-001: mypy zum blockierenden CI-Gate machen" \
  --label "priority:P0" --label "epic:governance" \
  --body "Siehe specs/agent-governance/04-initial-task-queue.md (WQ-001). \
Akzeptanz: mypy-Restfehler behoben, continue-on-error in ci.yml entfernt, \
alle Quality Gates gruen."
```

Für jedes Issue: Kontext, prüfbare Akzeptanzkriterien, Dateien im/außer Scope angeben
(das Issue-Formular fragt das strukturiert ab).

### 4c 🧑 Aufgaben freigeben

Setze das Label **`agent-ready`** auf die Issues, die der Agent abarbeiten soll.
Empfehlung für den Start: nur WQ-001, WQ-002, WQ-003 freigeben, den Rest erst nach
dem ersten erfolgreichen Lauf. **Ohne `agent-ready` ist ein Issue für den Agenten
unsichtbar** — so steuerst du, *was* gemacht wird.

---

## Schritt 5 — Autonomen Workflow starten

🧑 **Trockenlauf:** GitHub → **Actions → agent-pick-next → Run workflow**
(`workflow_dispatch`). Der Agent sollte:

1. das oberste `agent-ready`-Issue wählen und `agent-in-progress` setzen,
2. einen Kurzplan als Issue-Kommentar posten,
3. einen Branch `agent/<nr>-<slug>` anlegen,
4. test-first implementieren, die Quality Gates grün machen,
5. einen Pull Request öffnen (`Closes #<nr>`) — **und stoppen**.

🧑 Du reviewst den PR und merged ihn (oder forderst Änderungen an).

Danach läuft es 🤖 automatisch:

- **Zeitplan:** werktags 06:00 UTC zieht `agent-pick-next` den nächsten Task.
- **Label:** sobald du ein Issue mit `agent-ready` labelst, startet sofort ein Lauf.
- **Nachbessern:** schlägt die CI auf einem `agent/*`-PR fehl oder kommt ein
  Review-Kommentar, reagiert `agent-pr-fix` und pusht einen Fix.

Cron-Kadenz nach Bedarf in `agent-pick-next.yml` (`cron:`) anpassen.

---

## Was läuft automatisch, was musst du anstoßen?

| Vorgang | Wer |
|---------|-----|
| CI bei Push/PR | 🤖 automatisch |
| Repo + Branches übertragen | 🧑 Schritt 0 |
| Lokale Umgebung einrichten | 🧑 Schritt 1 |
| Branch Protection für `main` | 🧑 Schritt 2 |
| GitHub-App + Azure/Foundry-Secrets | 🧑 Schritt 3 |
| Modellname in Workflows eintragen | 🧑 Schritt 3c |
| Labels + Seed-Issues anlegen | 🧑 Schritt 4 |
| Issue mit `agent-ready` freigeben | 🧑 Schritt 4c |
| Nächsten Task ziehen (Cron/Label) | 🤖 automatisch |
| Plan, Implementierung, Tests, PR | 🤖 automatisch |
| CI-Fehler / Review nachbessern | 🤖 automatisch |
| PR reviewen und mergen | 🧑 immer |

---

## Verifikations-Checkliste

- [ ] `main` und Arbeitsbranch im neuen Repo vorhanden
- [ ] Lokale Quality Gates grün
- [ ] CI-Workflow `ci` läuft grün
- [ ] Branch Protection auf `main` aktiv (`ci` als Required Check)
- [ ] GitHub-App installiert; ggf. `APP_ID` / `APP_PRIVATE_KEY` gesetzt
- [ ] Azure-Secrets + `ANTHROPIC_FOUNDRY_BASE_URL` gesetzt
- [ ] Modellname in beiden `agent-*.yml` eingetragen
- [ ] 9 Labels und Seed-Issues angelegt
- [ ] Mindestens ein Issue mit `agent-ready` freigegeben
- [ ] Trockenlauf von `agent-pick-next` erfolgreich (PR geöffnet, nicht gemerged)

---

## Weiterführend

- `specs/agent-governance/03-autonomous-agent-workflow.md` — Loop-Logik im Detail
- `specs/agent-governance/04-initial-task-queue.md` — Seed-Aufgaben
- `specs/agent-governance/01-ai-coding-guardrails.md` — verbindliche Agentenregeln
- `AGENTS.md` / `CLAUDE.md` — agentenübergreifender bzw. Claude-Code-Kontext
