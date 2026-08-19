#!/usr/bin/env bash
# Locate the plugin root across Claude Code, Codex, Grok Build, and Cursor.
set -euo pipefail
ROOT="${CLAUDE_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT:-}}}"
if [[ -z "${ROOT}" ]]; then
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
exec python3 "${ROOT}/hooks/run.py"
