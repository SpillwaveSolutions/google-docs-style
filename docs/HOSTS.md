# Hosts

## Three-host hooks

If Claude Code ships `hooks/hooks.json`, this plugin also ships:

- `hooks/codex-hooks.json` — Codex event map (same scripts; `ExitPlanMode` omitted)
- `hooks/cursor-hooks.json` — Cursor-native events (`postToolUse`, `afterFileEdit`, …)

`.cursor/rules/` remains soft guidance and is not a substitute for hooks.

## WikiTicket SDD

Track work with the worklog plugin (`SpillwaveSolutions/wiki_ticket_sdd`). See [WORKLOG.md](WORKLOG.md).
