# Claude Code Hooks

Dieses Verzeichnis enthält die in `.claude/settings.json` verdrahteten Hooks.
`settings.json` erlaubt keine Kommentare — daher werden Zweck und Verhalten hier
dokumentiert.

## Übersicht

| Hook | Event | Matcher | Zweck |
|------|-------|---------|-------|
| `prevent-sensitive-file-access.sh` | PreToolUse | `Read\|Edit\|Write` | Blockt Zugriff auf `.env*`, Keys, Credentials, Secret-Verzeichnisse |
| `format-after-edit.sh` | PostToolUse | `Edit\|Write` | Formatiert/lintet geänderte `.py`-Dateien mit `ruff` |

## Funktionsweise

Claude Code übergibt jedes Tool-Event als JSON auf `stdin`. Die Skripte parsen
`tool_input.file_path` (Fallback `tool_input.path`) mit `python3` (im Repo immer
verfügbar, Python 3.11+).

### `prevent-sensitive-file-access.sh`
Blockiert (Exit-Code `2`), wenn der Dateiname einem der Muster entspricht:
`.env`, `.env.*`, `*.pem`, `*.key`, `*credentials*`, `local.settings.json` oder der
Pfad ein `secrets/`-Verzeichnis enthält. Die stderr-Meldung wird an Claude
zurückgegeben. Lässt sich kein Pfad ermitteln, wird **nicht** blockiert (Exit `0`).
Dies ergänzt die `deny`-Regeln in `settings.json` als zweite Verteidigungslinie.

### `format-after-edit.sh`
Läuft nur für `.py`-Dateien. Führt `ruff format` und `ruff check --fix` für die
geänderte Datei aus. Defensiv: bricht nie hart ab; ist `ruff` nicht installiert oder
die Datei nicht vorhanden, wird der Hook ohne Fehler übersprungen.

## Portabilität

- Skripte sind für Linux/macOS (`bash`, POSIX-Tools, `python3`) geschrieben.
- Unter Windows greifen Hooks ggf. nicht; dort gelten die Regeln aus `AGENTS.md`
  und die CI-Gates weiterhin.
- Hooks wirken nur in Claude Code. Andere Agenten (Codex, Cursor, Copilot) werden
  über `AGENTS.md` und CI abgesichert.

## Aktivierung / Test

Die Hooks sind über `.claude/settings.json` aktiv. Manuelle Prüfung:

```bash
bash -n .claude/hooks/prevent-sensitive-file-access.sh   # Syntaxcheck
echo '{"tool_input":{"file_path":".env"}}' | .claude/hooks/prevent-sensitive-file-access.sh; echo "exit=$?"   # erwartet exit=2
echo '{"tool_input":{"file_path":"src/ea_assistant/main.py"}}' | .claude/hooks/prevent-sensitive-file-access.sh; echo "exit=$?"   # erwartet exit=0
```

Nach dem Klonen müssen die Skripte ausführbar sein (`chmod +x .claude/hooks/*.sh`).
