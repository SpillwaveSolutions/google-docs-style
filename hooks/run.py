#!/usr/bin/env python3
"""Universal hook entrypoint for Claude Code, Codex, Cursor, and Grok Build."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from google_docs_style import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(["--hook"]))
