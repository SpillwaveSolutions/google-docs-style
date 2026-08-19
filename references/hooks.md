# Hooks and first-class plugin adapters

This plugin ships one formatter and native plugin manifests. Each host loads
its own manifest. All hosts call `hooks/run.sh`.

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

The shared `hooks/hooks.json` command is:

```bash
bash "${CLAUDE_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT}}}"/hooks/run.sh
```

Codex also sets `CLAUDE_PLUGIN_ROOT` for compatibility.

## Grok Build

- Manifest: `.grok-plugin/plugin.json`
- Marketplace: `.grok-plugin/marketplace.json`
- Hooks: `hooks/hooks.json`
- Env: `GROK_PLUGIN_ROOT`, `GROK_PLUGIN_DATA`

Install:

```bash
grok plugin install https://github.com/SpillwaveSolutions/google-docs-style --trust
```

## Claude Code

- Manifest: `.claude-plugin/plugin.json`
- Marketplace: `.claude-plugin/marketplace.json` (`source: "./"`)
- Hooks: `hooks/hooks.json`
- Output style: `output-styles/google-docs.md`
- Commands: `commands/`
- Env: `CLAUDE_PLUGIN_ROOT`

Install:

```text
/plugin marketplace add SpillwaveSolutions/google-docs-style
/plugin install google-docs-style@spillwave-google-docs-style
```

## Codex

- Manifest: `.codex-plugin/plugin.json`
- Marketplace: `.agents/plugins/marketplace.json`
- Hooks: `hooks/hooks.json`
- Env: `PLUGIN_ROOT`

Install:

```bash
codex plugin marketplace add SpillwaveSolutions/google-docs-style
```

Enable hooks in Codex if your build requires `features.codex_hooks`.

## Cursor

- Manifest: `.cursor-plugin/plugin.json`
- Project hooks: `.cursor/hooks.json`
- Adapter: `adapters/cursor/hooks.json`

## Universal plugin

`plugin.json` follows [Agent Plugins v1](https://agent-plugins.org/specification).
Host manifests sit under `extensions`.
