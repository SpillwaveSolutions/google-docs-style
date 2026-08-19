#!/usr/bin/env python3
"""CLI alias: format markdown files in place."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from google_docs_style import main

if __name__ == "__main__":
    raise SystemExit(main())
