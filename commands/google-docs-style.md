---
name: google-docs-style
description: Apply Google developer documentation style to the current plan or document.
---

Load the `google-docs-style` skill.

Rewrite the current plan or document to follow the Google developer documentation style guide.

Rules:
- Second person, present tense, active voice
- Sentence case headings and one H1
- Numbered lists for sequences
- No em dashes
- Bold UI labels, code font for code and filenames

Then run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT:-.}/scripts/google_docs_style.py --lint PATH
```

Fix remaining lint before you stop.
