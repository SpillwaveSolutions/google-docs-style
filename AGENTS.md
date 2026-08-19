# Agent instructions

This repository is the `google-docs-style` universal agent plugin.

## Purpose

Write plans and documents in Google developer documentation style. Use the same standard on Codex, Claude Code, Cursor, and Grok Build.

## Required style

- Second person, present tense, active voice
- Sentence case headings, one H1, no skipped heading levels
- Numbered lists for sequences, bullets otherwise
- Serial comma, American spelling
- Bold UI labels, code font for code and filenames
- No em dashes
- Do not start sentences with So, That, Thus, or Hence

## Commands

```bash
python3 scripts/google_docs_style.py path/to/doc.md
python3 scripts/google_docs_style.py --lint --check path/to/doc.md
python3 tests/test_formatter.py
```

## Layout

- `SKILL.md` is the skill contract.
- `scripts/google_docs_style.py` is the formatter and hook runner.
- `hooks/` is the Claude Code and Grok Build hook bundle.
- `adapters/cursor/` is the Cursor hook adapter.
- `adapters/codex/` is the Codex hook adapter.

When writing or editing `*.md` under `docs/`, `plans/`, or well-known doc filenames, apply this style automatically.
