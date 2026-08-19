# Google docs style

[![Agent Plugins v1](https://img.shields.io/badge/Agent%20Plugins-v1-0F9D58)](https://agent-plugins.org/specification)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-SKILL.md-4285F4)](https://agentskills.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Universal agent plugin for the
[Google developer documentation style guide](https://developers.google.com/style).

The plugin standardizes planning and documents across Claude Code, Codex,
Cursor, and Grok Build. One skill, one formatter, and platform hooks share
the same rules.

## Features

- Skill that teaches agents to write Google-style docs and plans
- Custom output formatter and linter for markdown
- Hooks for Claude Code, Codex, Cursor, and Grok Build
- Agent Plugins v1 `plugin.json` for universal install
- Templates for plans, how-tos, concepts, and reference pages

## Installing with Skilz

```bash
skilz install https://github.com/SpillwaveSolutions/google-docs-style
```

Or:

```bash
skilz install SpillwaveSolutions_google-docs-style/google-docs-style
```

Browse the skill on the Skilz marketplace after it is indexed.

## Install by platform

### Claude Code

Install this repository as a plugin. Hooks load from `hooks/hooks.json`.

```bash
# Example: add the marketplace or local plugin path, then enable google-docs-style
```

### Codex

Point Codex at this plugin. Hooks live in `adapters/codex/hooks.json`.
The Codex plugin manifest is `.codex-plugin/plugin.json`.

Enable Codex hooks if your CLI requires `features.codex_hooks`.

### Cursor

Copy the Cursor adapter into the project:

```bash
mkdir -p .cursor
cp adapters/cursor/hooks.json .cursor/hooks.json
```

Cursor events: `sessionStart`, `beforeSubmitPrompt`, `preToolUse`,
`afterFileEdit`, `stop`. All of them call the shared formatter.

### Grok Build

Install the plugin with Grok Build, or copy `adapters/grok/hooks.json` to
`.grok/hooks.json`. Plugin hooks receive `GROK_PLUGIN_ROOT`.

## Formatter

```bash
python3 scripts/google_docs_style.py docs/guide.md
python3 scripts/google_docs_style.py --lint --check docs/guide.md
python3 scripts/google_docs_style.py --reminder
```

The formatter rewrites sentence-case headings and em dashes. The linter
flags passive voice, first-person "we", weak sentence openers, missing H1,
and skipped heading levels.

## Style contract

- Second person, present tense, active voice
- Sentence case headings and a single H1
- Numbered lists for sequences
- Serial comma, American spelling
- Bold UI labels, code font for code
- No em dashes
- Plans use the same rules as product docs

Full rules: [references/google-developer-docs-style.md](references/google-developer-docs-style.md)

## Layout

```text
plugin.json                 Agent Plugins v1 manifest
SKILL.md                    Canonical skill
skills/google-docs-style/   Portable skills discovery path
hooks/                      Shared runner and Claude/Grok hook bundle
adapters/                   Cursor, Codex, Claude, Grok hook manifests
scripts/google_docs_style.py
templates/
references/
```

## Tests

```bash
python3 tests/test_formatter.py
```

## License

MIT. Style rules summarize the public Google developer documentation style
guide. Google owns that guide.
