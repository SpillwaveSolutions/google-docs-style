# Google developer documentation style rules

This file is a compact working subset of the public
[Google developer documentation style guide](https://developers.google.com/style).
Use it as the lint and generation contract for this plugin.

## Highlights

- Be conversational and clear.
- Write for a global audience.
- Use second person (`you`), not `we`.
- Use present tense.
- Use active voice.
- Use sentence case for titles and headings.
- Use numbered lists for sequences.
- Use bulleted lists for non-sequential items.
- Use the serial comma.
- Put UI elements in **bold**.
- Put code, commands, and filenames in `code font`.
- Follow American spelling and the Google word list.

## Headings

- One H1 per document. The H1 is the document title.
- Do not skip levels (H2 to H4 is invalid).
- Procedure headings use a bare infinitive: `Create a cluster`.
- Concept headings use a noun phrase: `Cluster architecture`.
- Sentence case: `Install the CLI`, not `Install The CLI`.
- Keep acronyms such as `API`, `HTTP`, and `JSON`.

## Voice examples

Do:

```markdown
Create a repository in the Spillwave Solutions organization.
```

Don't:

```markdown
A repository is created by the user.
We should create a repository.
```

## Punctuation

- Use a serial comma: `skills, hooks, and adapters`.
- Do not use em dashes. Split the sentence or use a comma.
- Use American quotation style.

## Lists

- Numbered: ordered steps, ranked items.
- Bullets: options, features, notes.
- Description lists: term and definition pairs.
- Introduce a list with a complete sentence and a colon.

## Code and UI

- Inline code for files, flags, HTTP methods, and class names.
- Fenced blocks for commands and multi-line samples. Include a language tag.
- Bold for buttons, menus, and dialog names: Click **Save**.

## Planning overlay

Plans are documents. They follow this same style.

Required plan sections:

1. Outcome
2. Scope
3. Non-goals
4. Steps
5. Risks
6. Next action

## Formatter mapping

| Rule | Formatter action |
| --- | --- |
| Sentence case headings | Rewrite title case headings |
| Em dashes | Replace with a period or comma |
| Active voice | Lint only |
| Second person | Lint `we` / `let's` |
| Weak openers | Lint sentences that start with So, That, Thus, Hence |
| One H1 | Lint missing or multiple H1s |
| Heading skip | Lint |

Source: https://developers.google.com/style/highlights
