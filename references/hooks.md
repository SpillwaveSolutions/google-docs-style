# Hooks and adapters

This plugin ships one formatter and several hook manifests. Each platform
loads the adapter that matches its hook contract. All adapters call
`hooks/run.sh`, which runs `hooks/run.py`.

## Shared runner

`hooks/run.py` reads hook JSON on stdin and:

1. Injects the style reminder on session start and prompt submit
2. Injects the reminder before Write/Edit when the path looks like a document
3. Formats the file after Write/Edit and returns leftover lint

Document paths include `*.md`, `README.md`, `AGENTS.md`, and files under
`docs/`, `plans/`, `design/`, and `adr/`.

Plugin root discovery order:

1. `CLAUDE_PLUGIN_ROOT`
2. `GROK_PLUGIN_ROOT`
3. `PLUGIN_ROOT`
4. Parent of `hooks/`

## Claude Code

- Manifest: `.claude-plugin/plugin.json`
- Hooks: `hooks/hooks.json` and `adapters/claude/hooks.json`
- Events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`
- Env: `CLAUDE_PLUGIN_ROOT`

## Codex

- Manifest: `.codex-plugin/plugin.json`
- Hooks: `adapters/codex/hooks.json`
- Events: `SessionStart`, `UserPromptSubmit`, `PreToolUse` (`Write|Edit|apply_patch`), `PostToolUse`, `Stop`
- Env: `PLUGIN_ROOT`
- Enable hooks in Codex if your build requires `features.codex_hooks`.

## Cursor

- Project file: `.cursor/hooks.json`
- Adapter: `adapters/cursor/hooks.json`
- Events: `sessionStart`, `beforeSubmitPrompt`, `preToolUse`, `afterFileEdit`, `stop`
- Copy `adapters/cursor/hooks.json` to `.cursor/hooks.json` in the target repo, or install this repository as a Cursor plugin.

Cursor is part of the universal agent plugin standard. The Cursor adapter
registers the same formatter used by Codex, Claude Code, and Grok Build.

## Grok Build

- Adapter: `adapters/grok/hooks.json`
- Project file: `.grok/hooks.json`
- Events match the Claude-compatible set
- Env: `GROK_PLUGIN_ROOT`, `GROK_PLUGIN_DATA`

## Universal plugin

`plugin.json` follows [Agent Plugins v1](https://agent-plugins.org/specification).
Client-specific hook paths sit under `extensions`.

Skilz install uses the root `SKILL.md`:

```bash
skilz install https://github.com/SpillwaveSolutions/google-docs-style
```
