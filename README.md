# Google docs style

[![Agent Plugins v1](https://img.shields.io/badge/Agent%20Plugins-v1-0F9D58)](https://agent-plugins.org/specification)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-d97706)](https://code.claude.com/docs/en/plugins)
[![Codex Plugin](https://img.shields.io/badge/Codex-Plugin-10A37F)](https://developers.openai.com/plugins/build/plugins)
[![Grok Build Plugin](https://img.shields.io/badge/Grok%20Build-Plugin-000000)](https://docs.x.ai/build/features/skills-plugins-marketplaces)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

First-class plugin for Claude Code, Codex, and Grok Build. Cursor hooks are included. The plugin applies the
[Google developer documentation style guide](https://developers.google.com/style)
to plans and documents.

One skill, one formatter, native manifests, slash commands, a Claude output style, and lifecycle hooks.

## Native plugin manifests

| Host | Manifest | Marketplace |
| --- | --- | --- |
| Grok Build | [`.grok-plugin/plugin.json`](.grok-plugin/plugin.json) | [`.grok-plugin/marketplace.json`](.grok-plugin/marketplace.json) |
| Claude Code | [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) |
| Codex | [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) | [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) |
| Cursor | [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json) | [`.cursor/hooks.json`](.cursor/hooks.json) |
| Universal | [`plugin.json`](plugin.json) (Agent Plugins v1) | Skilz |

## Install as a Grok Build plugin

```bash
grok plugin install https://github.com/SpillwaveSolutions/google-docs-style --trust
```

Or add this repo as a marketplace, then install `google-docs-style`:

```bash
grok plugin marketplace add SpillwaveSolutions/google-docs-style
```

Grok loads `skills/`, `commands/`, `agents/`, and `hooks/hooks.json`. Plugin hooks receive `GROK_PLUGIN_ROOT`.

## Install as a Claude Code plugin

```text
/plugin marketplace add SpillwaveSolutions/google-docs-style
/plugin install google-docs-style@spillwave-google-docs-style
```

Claude loads the skill, `/google-docs-style`, `/format-docs`, `/write-plan`, the `docs-writer` subagent, the `google-docs` output style, and hooks.

Enable the output style:

```text
/output-style google-docs
```

## Install as a Codex plugin

```bash
codex plugin marketplace add SpillwaveSolutions/google-docs-style
```

The Codex manifest points at `./skills/` and `./hooks/hooks.json`. Enable Codex hooks if your CLI requires `features.codex_hooks`. Plugin hooks receive `PLUGIN_ROOT` (and `CLAUDE_PLUGIN_ROOT` for compatibility).

## Installing with Skilz

```bash
skilz install https://github.com/SpillwaveSolutions/google-docs-style
```

## Cursor

```bash
mkdir -p .cursor
cp adapters/cursor/hooks.json .cursor/hooks.json
```

Cursor events call the same `hooks/run.sh` runner.

## What the plugin ships

| Component | Path |
| --- | --- |
| Skill | `skills/google-docs-style/SKILL.md` |
| Slash commands | `commands/` |
| Docs writer subagent | `agents/docs-writer.md` |
| Claude output style | `output-styles/google-docs.md` |
| Hooks | `hooks/hooks.json` |
| Formatter | `scripts/google_docs_style.py` |
| Templates | `templates/` |

## Style contract

- Second person, present tense, active voice
- Sentence case headings and a single H1
- Numbered lists for sequences
- Serial comma, American spelling
- Bold UI labels, code font for code
- No em dashes
- Plans use the same rules as product docs

## Formatter

```bash
python3 scripts/google_docs_style.py docs/guide.md
python3 scripts/google_docs_style.py --lint --check docs/guide.md
python3 tests/test_formatter.py
```

## License

MIT. Style rules summarize the public Google developer documentation style
guide. Google owns that guide.
