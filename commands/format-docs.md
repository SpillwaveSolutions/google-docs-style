---
name: format-docs
description: Format markdown files with the Google docs style formatter.
argument-hint: "[path]"
---

Format the markdown at `$ARGUMENTS` (or the files you just wrote) with the plugin formatter.

```bash
python3 ${CLAUDE_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT:-.}}}/scripts/google_docs_style.py $ARGUMENTS
python3 ${CLAUDE_PLUGIN_ROOT:-${GROK_PLUGIN_ROOT:-${PLUGIN_ROOT:-.}}}/scripts/google_docs_style.py --lint --check $ARGUMENTS
```

Report remaining lint findings and fix them.
