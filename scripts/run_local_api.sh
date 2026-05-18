#!/usr/bin/env bash
set -euo pipefail
uvicorn ea_assistant.main:app --reload
