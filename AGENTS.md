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

<!-- worklog:policy:start -->
## WikiTicket SDD (worklog)

This plugin tracks implementation with [WikiTicket SDD](https://github.com/SpillwaveSolutions/wiki_ticket_sdd).

- Install the `worklog` plugin from `SpillwaveSolutions/wiki_ticket_sdd` (Claude Code, Grok Build, Codex, Cursor).
- Config lives in `.work/config.yml`. Event log is `.work/todo.jsonl`.
- Every plan MUST end by running `worklog plan-capture`.
- Work discovered mid-flight: `worklog add --unplanned --discovered-during <item>` BEFORE doing the work.
- Never hand-edit `.work/*.jsonl` (use `worklog`) or `docs/roadmap.md` (generated).
- After changing work items, run `worklog roadmap-render` and commit the log and roadmap together.
- CLI: `worklog` on PATH, or `python3 <wiki_ticket_sdd>/bin/worklog`.
<!-- worklog:policy:end -->

