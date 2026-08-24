---
name: google-docs-style
description: Write and format planning docs, design docs, READMEs, ADRs, and technical documentation using the Google developer documentation style guide. Use when asked for Google documentation format, Google style docs, planning documents, how-to guides, or consistent docs across Claude Code, Codex, Cursor, and Grok Build.
license: MIT
metadata:
  author: Spillwave Solutions
  version: "1.1.0"
  organization: SpillwaveSolutions
---

# Google developer documentation style

Apply the [Google developer documentation style guide](https://developers.google.com/style) to every plan and document this agent writes.

This skill is the source of truth. Platform hooks inject the same rules before planning and before writing docs.

## Exclusive with STE100

`google-docs-style` and `ste100` are alternate voice packs. Use exactly one
per document. Do not mix them.

`document-specialist` defaults to STE100. Activate this skill only when the
user names Google style, Google developer docs, or the Google style guide.

Hard bans that still apply here:

- No em dash (`—`) and no `--` used as an em dash.
- Do not start a sentence with **So**, **That**, **Thus**, or **Hence**.

## When to use this skill

Use this skill when you:

- Write a plan, design doc, README, ADR, how-to, or reference page
- Format existing markdown to Google style
- Need one output standard across Codex, Claude Code, Cursor, and Grok Build

## Output contract

Every planning document and every technical document must follow these rules.

### Voice

- Address the reader as **you**.
- Use present tense and active voice.
- Use standard American spelling.
- Use the serial comma.
- Keep sentences short and concrete.
- Do not start a sentence with **So**, **That**, **Thus**, or **Hence**.
- Do not use em dashes. Use a period or a comma.

### Structure

- Use exactly one H1. Use sentence case for every heading.
- Do not skip heading levels.
- Prefer task headings for procedures (`Create a repository`).
- Prefer noun phrases for conceptual sections (`Repository layout`).
- Use numbered lists for sequences. Use bullets for everything else.
- Put UI labels in **bold**. Put code, commands, flags, and filenames in `code font`.

### Planning documents

- Lead with the outcome.
- State scope, non-goals, and the next action.
- Use the [plan template](templates/plan.md).

### How-to documents

- List prerequisites first.
- Number the steps.
- Show expected results after critical steps.
- Use the [how-to template](templates/how-to.md).

### Concept and reference documents

- Define the thing before you describe options.
- Keep reference pages scannable.
- Use [templates/concept.md](templates/concept.md) and [templates/reference.md](templates/reference.md).

## Formatter

Run the shared formatter on markdown before you consider a document done:

```bash
python3 scripts/google_docs_style.py path/to/doc.md
python3 scripts/google_docs_style.py --lint --check path/to/doc.md
```

The formatter:

- Converts title-case headings to sentence case
- Replaces em dashes
- Lints for passive voice, first-person "we", missing H1, skipped heading levels, and weak sentence openers

Do not rewrite fenced code blocks.

## Hooks

Hooks keep planning and documents on the same standard even when the skill is not explicitly invoked.

| Event | Action |
| --- | --- |
| Session start | Inject the style reminder |
| User prompt submit | Inject the style reminder for planning and docs |
| Pre Write/Edit | Inject the reminder when the target looks like a document |
| Post Write/Edit | Format the file and report leftover lint |

Adapters live in `adapters/` for Claude Code, Codex, Cursor, and Grok Build. See [references/hooks.md](references/hooks.md).

## Workflow

1. Choose the document type (plan, how-to, concept, reference).
2. Copy the matching template from `templates/`.
3. Write in Google style.
4. Run `scripts/google_docs_style.py`.
5. Fix remaining lint.

## References

- [Style rules](references/google-developer-docs-style.md)
- [Hooks and adapters](references/hooks.md)
- [Google developer documentation style guide](https://developers.google.com/style)
- [Highlights](https://developers.google.com/style/highlights)
