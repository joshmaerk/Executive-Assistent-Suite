#!/usr/bin/env bash
# PostToolUse hook: formatiert/lintet geänderte Python-Dateien nach Edit/Write.
# Defensiv: bricht nie hart ab; no-op wenn ruff oder die Datei fehlt.
set -euo pipefail

input="$(cat || true)"

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

# Nur Python-Dateien behandeln.
case "$file_path" in
  *.py) ;;
  *) exit 0 ;;
esac

[ -f "$file_path" ] || exit 0

if ! command -v ruff >/dev/null 2>&1; then
  echo "format-after-edit: ruff nicht gefunden — übersprungen." >&2
  exit 0
fi

ruff format "$file_path" >/dev/null 2>&1 || true
ruff check --fix "$file_path" >/dev/null 2>&1 || true

exit 0
