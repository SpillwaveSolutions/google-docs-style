#!/usr/bin/env python3
"""Google developer documentation style formatter and linter.

Implements a practical subset of
https://developers.google.com/style for agent-written plans and docs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


DOC_EXTENSIONS = {".md", ".mdx", ".rst", ".txt", ".adoc"}
DOC_PATH_HINTS = (
    "/docs/",
    "/doc/",
    "/plans/",
    "/plan/",
    "/design/",
    "/adr/",
    "/wiki/",
    "/references/",
)
DOC_BASENAMES = {
    "readme.md",
    "agents.md",
    "claude.md",
    "gemini.md",
    "contributing.md",
    "changelog.md",
    "architecture.md",
    "design.md",
    "plan.md",
    "roadmap.md",
    "spec.md",
}

SMALL_WORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "for",
    "nor",
    "on",
    "in",
    "at",
    "to",
    "from",
    "by",
    "of",
    "as",
    "is",
    "if",
    "via",
    "with",
    "without",
    "into",
    "onto",
}
ACRONYMS = {
    "API",
    "APIs",
    "HTTP",
    "HTTPS",
    "JSON",
    "YAML",
    "HTML",
    "CSS",
    "SQL",
    "SDK",
    "CLI",
    "UI",
    "UX",
    "ID",
    "IDs",
    "URL",
    "URLs",
    "URI",
    "CPU",
    "GPU",
    "OS",
    "AI",
    "LLM",
    "MCP",
    "ADR",
    "PR",
    "PRs",
    "CI",
    "CD",
    "SSH",
    "TLS",
    "TCP",
    "UDP",
    "REST",
    "gRPC",
    "OAuth",
    "JWT",
    "AWS",
    "GCP",
    "SKU",
    "SKILL",
}

PASSIVE_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?"
    r"(?:done|made|used|created|written|called|performed|executed|provided|"
    r"shown|given|taken|set|updated|added|removed|installed|configured|"
    r"implemented|generated|returned)\b",
    re.IGNORECASE,
)
WE_RE = re.compile(r"\b(?:we|we're|we've|we'll|let's|lets)\b", re.IGNORECASE)
EMDASH_RE = re.compile(r"\s*[—–]\s*|\s+--\s+")
TITLE_WORD_RE = re.compile(r"^[A-Z][a-z0-9']+$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
FENCE_RE = re.compile(r"^```")


@dataclass
class Finding:
    line: int
    rule: str
    message: str
    excerpt: str


def is_doc_path(path: str | None) -> bool:
    if not path:
        return False
    normalized = path.replace("\\", "/").lower()
    suffix = Path(normalized).suffix
    name = Path(normalized).name
    if name in DOC_BASENAMES:
        return True
    if suffix in DOC_EXTENSIONS:
        return True
    return any(hint in f"/{normalized}/" or hint in normalized for hint in DOC_PATH_HINTS)


def sentence_case_heading(text: str) -> str:
    """Convert a heading to sentence case, preserving acronyms and inline code."""
    if text.startswith("`") or text.isupper():
        return text
    words = text.split(" ")
    if len(words) < 2:
        return text
    titled = 0
    candidates = 0
    for word in words[1:]:
        bare = word.strip(".,:;!?()[]{}")
        if not bare or bare.startswith("`") or bare.startswith("[") or bare in ACRONYMS:
            continue
        candidates += 1
        if TITLE_WORD_RE.match(bare) and bare not in {"I"}:
            titled += 1
    if candidates == 0 or titled / candidates < 0.6:
        return text

    out = []
    for i, word in enumerate(words):
        lead = re.match(r"^[^A-Za-z0-9`]*", word).group(0)
        trail = re.search(r"[^A-Za-z0-9`]*$", word).group(0)
        core = word[len(lead) : len(word) - len(trail) if trail else len(word)]
        if not core:
            out.append(word)
            continue
        if core.startswith("`") or core in ACRONYMS or "/" in core or (core.isupper() and len(core) > 1):
            out.append(word)
            continue
        if i == 0:
            new_core = core[0].upper() + core[1:] if core else core
        elif core.lower() in SMALL_WORDS or TITLE_WORD_RE.match(core):
            new_core = core.lower()
        else:
            new_core = core
        out.append(f"{lead}{new_core}{trail}")
    return " ".join(out)


def replace_em_dashes(text: str) -> str:
    spans = list(EMDASH_RE.finditer(text))
    if not spans:
        return text
    rebuilt = []
    last = 0
    for span in spans:
        rebuilt.append(text[last : span.start()])
        left = text[: span.start()].rstrip()
        right = text[span.end() :].lstrip()
        if (right[:1].isupper() and left) or left.endswith((".", "!", "?")):
            rebuilt.append(". ")
        else:
            rebuilt.append(", ")
        last = span.end()
    rebuilt.append(text[last:])
    result = "".join(rebuilt)
    result = re.sub(r"\.\s+\.", ".", result)
    result = re.sub(r",\s+,", ",", result)
    return result


def _in_fence(lines: list[str], index: int) -> bool:
    fences = 0
    for i in range(index):
        if lines[i].lstrip().startswith("```"):
            fences += 1
    return fences % 2 == 1


def format_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n")
    lines = text.split("\n")
    out: list[str] = []
    for i, line in enumerate(lines):
        if _in_fence(lines, i):
            out.append(line)
            continue
        heading = HEADING_RE.match(line)
        if heading:
            level, title = heading.group(1), heading.group(2)
            title = replace_em_dashes(title)
            title = sentence_case_heading(title)
            out.append(f"{level} {title}")
            continue
        out.append(replace_em_dashes(line))
    formatted = "\n".join(out)
    formatted = re.sub(r"\n{4,}", "\n\n\n", formatted)
    if formatted and not formatted.endswith("\n"):
        formatted += "\n"
    return formatted


def lint_markdown(text: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.replace("\r\n", "\n").split("\n")
    heading_levels: list[int] = []
    h1_count = 0
    for i, line in enumerate(lines, start=1):
        if _in_fence(lines, i - 1):
            continue
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2)
            heading_levels.append(level)
            if level == 1:
                h1_count += 1
            converted = sentence_case_heading(title)
            if converted != title:
                findings.append(
                    Finding(i, "heading-sentence-case", "Use sentence case for headings.", title)
                )
            if heading_levels and level > heading_levels[0] and heading_levels[-2:] and len(heading_levels) > 1:
                prev = heading_levels[-2]
                if level > prev + 1:
                    findings.append(
                        Finding(
                            i,
                            "heading-skip",
                            "Do not skip heading levels.",
                            title,
                        )
                    )
        if EMDASH_RE.search(line):
            findings.append(
                Finding(i, "em-dash", "Avoid em dashes. Use a period or comma.", line.strip())
            )
        if PASSIVE_RE.search(line) and not heading:
            findings.append(
                Finding(i, "active-voice", "Prefer active voice.", line.strip())
            )
        if WE_RE.search(line) and not heading:
            findings.append(
                Finding(
                    i,
                    "second-person",
                    'Prefer second person ("you") over first person ("we").',
                    line.strip(),
                )
            )
        if re.match(r"^(So|That|Thus|Hence)\b", line.strip()):
            findings.append(
                Finding(
                    i,
                    "weak-opener",
                    "Do not start a sentence with So, That, Thus, or Hence.",
                    line.strip(),
                )
            )
    if h1_count == 0:
        findings.append(Finding(1, "missing-h1", "Give the document a single H1 title.", ""))
    if h1_count > 1:
        findings.append(Finding(1, "multiple-h1", "Use exactly one H1 per document.", ""))
    return findings


def style_reminder() -> str:
    return """Follow the Google developer documentation style guide for plans and documents.

Voice and grammar:
- Use second person ("you"), present tense, and active voice.
- Use standard American spelling and the serial comma.
- Do not start sentences with So, That, Thus, or Hence.
- Do not use em dashes. Use a period or a comma.

Structure:
- Use one H1. Use sentence case for all headings.
- Do not skip heading levels.
- Use numbered lists for sequences. Use bullets for non-sequential lists.
- Put UI elements in bold. Put code, commands, and filenames in code font.

Planning and docs:
- Lead with the task or outcome.
- Keep sentences short and concrete.
- Prefer task headings ("Create a repository") over noun headings when the section is a procedure.
"""


def hook_payload_from_stdin(raw: str) -> dict:
    raw = raw.strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"_raw": raw}


def extract_path(payload: dict) -> str | None:
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    if isinstance(tool_input, dict):
        for key in ("file_path", "path", "filePath", "target_file", "filename"):
            value = tool_input.get(key)
            if isinstance(value, str) and value:
                return value
        updates = tool_input.get("updates") or tool_input.get("files")
        if isinstance(updates, list) and updates:
            first = updates[0]
            if isinstance(first, dict):
                return first.get("path") or first.get("file_path")
    for key in ("file_path", "path", "filePath"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def looks_like_planning_prompt(text: str) -> bool:
    if not text:
        return False
    lowered = text.lower()
    keywords = (
        "plan",
        "design doc",
        "design document",
        "write docs",
        "documentation",
        "readme",
        "architecture",
        "adr",
        "spec",
        "how-to",
        "google docs style",
        "google documentation",
    )
    return any(k in lowered for k in keywords)


def additional_context_response(event_name: str, context: str) -> dict:
    return {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": context,
            "additional_context": context,
        },
        "additional_context": context,
    }


def run_hook(payload: dict) -> dict | None:
    event = (
        payload.get("hook_event_name")
        or payload.get("hookEventName")
        or payload.get("event")
        or ""
    )
    event_l = str(event)

    if event_l in {"SessionStart", "sessionStart"}:
        return additional_context_response(event_l, style_reminder())

    if event_l in {"UserPromptSubmit", "beforeSubmitPrompt"}:
        prompt = payload.get("prompt") or payload.get("user_prompt") or ""
        if looks_like_planning_prompt(prompt) or True:
            # Always inject a short reminder. Planning and docs share one standard.
            return additional_context_response(event_l, style_reminder())
        return None

    path = extract_path(payload)
    if event_l in {"PreToolUse", "preToolUse"}:
        if is_doc_path(path):
            return additional_context_response(event_l, style_reminder())
        return None

    if event_l in {"PostToolUse", "postToolUse", "afterFileEdit", "stop", "Stop"}:
        if path and is_doc_path(path) and Path(path).exists():
            original = Path(path).read_text(encoding="utf-8")
            formatted = format_markdown(original)
            if formatted != original:
                Path(path).write_text(formatted, encoding="utf-8")
            findings = lint_markdown(formatted)
            if findings:
                summary = "\n".join(
                    f"- L{f.line} [{f.rule}] {f.message}" for f in findings[:12]
                )
                return additional_context_response(
                    event_l,
                    "Google docs style lint after write:\n" + summary,
                )
        return None

    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Google docs style formatter and hook runner")
    parser.add_argument("paths", nargs="*", help="Markdown files to format or lint")
    parser.add_argument("--lint", action="store_true", help="Lint instead of rewrite")
    parser.add_argument("--hook", action="store_true", help="Read hook JSON from stdin")
    parser.add_argument("--reminder", action="store_true", help="Print the style reminder")
    parser.add_argument("--check", action="store_true", help="Exit 1 if lint findings exist")
    parser.add_argument("--json", action="store_true", help="Print findings as JSON")
    args = parser.parse_args(argv)

    if args.reminder:
        sys.stdout.write(style_reminder())
        return 0

    if args.hook:
        raw = sys.stdin.read()
        payload = hook_payload_from_stdin(raw)
        result = run_hook(payload)
        if result:
            json.dump(result, sys.stdout)
            sys.stdout.write("\n")
        return 0

    if not args.paths:
        parser.print_help()
        return 2

    all_findings: list[dict] = []
    failed = False
    for path_str in args.paths:
        path = Path(path_str)
        text = path.read_text(encoding="utf-8")
        if args.lint or args.check:
            findings = lint_markdown(text)
            if args.json:
                all_findings.extend({"file": str(path), **asdict(f)} for f in findings)
            else:
                for finding in findings:
                    print(f"{path}:{finding.line}: {finding.rule}: {finding.message}")
            if findings:
                failed = True
        else:
            formatted = format_markdown(text)
            if formatted != text:
                path.write_text(formatted, encoding="utf-8")
                print(f"formatted {path}")
            findings = lint_markdown(formatted)
            if args.json:
                all_findings.extend({"file": str(path), **asdict(f)} for f in findings)
            elif findings:
                for finding in findings:
                    print(f"{path}:{finding.line}: {finding.rule}: {finding.message}")
            if args.check and findings:
                failed = True

    if args.json:
        json.dump(all_findings, sys.stdout, indent=2)
        sys.stdout.write("\n")
    return 1 if failed and args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
