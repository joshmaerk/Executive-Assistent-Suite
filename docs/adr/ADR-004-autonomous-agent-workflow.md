# ADR-004: Autonomous Agent Workflow

## Status

Accepted

## Context

Das Repo soll von AI-Coding-Agenten weiterentwickelt werden, ohne dass ein Mensch
jede Session manuell startet. Benötigt wird eine versionierte Mechanik, die Aufgaben
auswählt, plant, umsetzt, testet, nachbessert und die nächste Aufgabe nimmt — bei
gleichzeitig erhaltener menschlicher Kontrolle und deterministischer Absicherung.

Abgrenzung: `AGENTS.md` untersagt den Bau eines Produkt-Agenten-Frameworks vor dem
stabilen MVP. Diese Entscheidung betrifft ausschließlich Dev-Infrastruktur
(CI/Automatisierung), kein Produktfeature.

## Decision

Es wird ein autonomer Agenten-Workflow eingeführt:

- **Work Queue = GitHub Issues** mit Labels (`agent-ready`, `agent-in-progress`,
  `agent-blocked`, `priority:*`, `epic:*`). Ein Mensch gibt Aufgaben per
  `agent-ready` frei.
- **Trigger = GitHub Actions** mit `anthropics/claude-code-action@v1`, authentifiziert
  über Azure / Microsoft Foundry (OIDC). Zwei Workflows:
  `agent-pick-next.yml` (Cron + manuell + neues `agent-ready`-Label) und
  `agent-pr-fix.yml` (fehlgeschlagene CI / Review-Kommentar auf `agent/*`-PRs).
- **Logik** liegt versioniert in `specs/agent-governance/03-autonomous-agent-workflow.md`;
  die Workflow-YAMLs verweisen nur kurz darauf.
- **Ein Lauf = ein Issue.** Der Agent öffnet einen PR und stoppt; ein Mensch merged.

## Rationale

- GitHub Issues sind nativ triggerbar, sichtbar und konfliktfrei — besser als eine
  versionierte Queue-Datei.
- Pro-Lauf-ein-Issue ist robuster als ein dauerlaufender Prozess und passt zur
  Realität von GitHub Actions.
- Die Autonomiegrenze „Agent öffnet PR, Mensch merged" erhält eine menschliche
  Kontrollinstanz und passt zur Human-in-the-loop-Governance des Repos.
- Logik im versionierten Spec-Dokument statt im YAML folgt der Repo-Philosophie
  (lange Arbeitsweisen gehören in Workflows/Skills).

## Consequences

- Einmalige menschliche Einrichtung nötig: GitHub-App, Azure/Foundry-OIDC + Secrets,
  Branch Protection für `main`. Ohne diese laufen die Workflows nicht (beabsichtigt).
- Autonome Läufe verursachen API-/Actions-Kosten → konservativer Cron, `--max-turns`
  und `timeout-minutes` als Caps, `concurrency` gegen Parallelläufe.
- CI und der menschliche Merge bleiben die deterministischen Gates gegen
  probabilistische Agentenfehler; Branch Protection ist Pflicht.
- Die exakten Foundry-Inputs der Action können je Version abweichen und müssen
  gegen die gepinnte Version verifiziert werden (TODO-Kommentare in den Workflows).
