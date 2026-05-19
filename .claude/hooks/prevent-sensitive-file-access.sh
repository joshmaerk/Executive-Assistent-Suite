#!/usr/bin/env bash
# PreToolUse hook: blockt Lese-/Schreibzugriff auf sensible Dateien.
# Claude Code übergibt das Tool-Event als JSON auf stdin.
# Exit 0 = erlaubt, Exit 2 = blockiert (stderr-Meldung geht an Claude).
set -euo pipefail

input="$(cat || true)"

# Dateipfad aus tool_input extrahieren (file_path, sonst path).
file_path="$(
  printf '%s' "$input" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    print("")
    sys.exit(0)
ti = data.get("tool_input", {}) or {}
print(ti.get("file_path") or ti.get("path") or "")
' 2>/dev/null || true
)"

# Kein Pfad ermittelbar -> nicht blockieren.
if [ -z "$file_path" ]; then
  exit 0
fi

base="$(basename "$file_path")"

case "$base" in
  .env|.env.*|*.pem|*.key|*credentials*|local.settings.json)
    echo "BLOCKED: Zugriff auf sensible Datei '$file_path' ist nicht erlaubt." >&2
    echo "Secrets/Keys gehören in Azure Key Vault / Managed Identity, nicht ins Repo." >&2
    exit 2
    ;;
esac

case "$file_path" in
  *secrets/*|*/secrets/*)
    echo "BLOCKED: Zugriff auf Secret-Verzeichnis ('$file_path') ist nicht erlaubt." >&2
    exit 2
    ;;
esac

exit 0
