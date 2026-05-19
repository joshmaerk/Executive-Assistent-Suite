# M365 Executive Assistant

Produktionsnahes MVP-Repository für einen kontrollierten Executive Assistant auf Basis von:

- Microsoft 365 / Outlook / Teams
- Power Automate mit HTTP Premium Connector
- Azure OpenAI / Azure AI Foundry
- Microsoft Graph für Drafts, Kategorien und feingranulare Outlook-Aktionen
- Human-in-the-loop-Freigabe für alle schreibenden Aktionen

## Ziel

Der Assistant unterstützt Führungskräfte bei:

1. Morning Briefing
2. Inbox Triage
3. Meeting Preparation
4. Follow-up Radar
5. Weekly Calendar Audit

Der MVP startet mit `EA_MorningBriefing`.

## Architekturprinzip

Power Automate bleibt dünn:

```text
Power Automate
  -> liest Kalender/E-Mails
  -> ruft Assistant API auf
  -> zeigt Teams Adaptive Card / Approval
  -> führt nach Freigabe Marker/Drafts aus
```

Die Businesslogik liegt versioniert im Repo:

```text
Prompts + Schemas + Guardrails + Evals + API
```

## MVP-Flow

```text
Recurrence Trigger
  -> Outlook: Kalender heute/morgen lesen
  -> Outlook: E-Mails seit gestern 16:00 lesen
  -> HTTP Premium: POST /api/v1/morning-briefing
  -> Parse JSON
  -> Teams Adaptive Card posten
  -> Nach Freigabe: Flag / Draft / Mark unread
```

## Nicht-Ziele im MVP

- Kein automatisches Senden von E-Mails
- Kein automatisches Verschieben/Absagen von Terminen
- Kein automatisches Löschen/Archivieren
- Keine autonome Kommunikation nach außen
- Keine Verarbeitung von Anhängen im ersten Schritt
- Keine SharePoint-/OneDrive-RAG im ersten Schritt

## Schnellstart lokal

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn ea_assistant.main:app --reload
```

Dann:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/morning-briefing \
  -H "Content-Type: application/json" \
  -d @prompts/morning_briefing/input_example.json
```

## Agent Build Spec

Die zentrale Spezifikation für KI-Coding-Agenten liegt in:

```text
AGENTS.md
specs/AI_AGENT_BUILD_SPEC.md
```

## Setup & autonomer Workflow

Schritt-für-Schritt-Anleitung, um das Projekt in einer GitHub-Instanz scharf zu
schalten (lokale Umgebung, CI, autonomer AI-Coding-Workflow):

```text
docs/SETUP.md
```
