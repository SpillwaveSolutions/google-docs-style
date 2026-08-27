#!/usr/bin/env python3
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from google_docs_style import (  # noqa: E402
    format_markdown,
    hook_payload_from_stdin,
    is_doc_path,
    lint_markdown,
    run_hook,
    sentence_case_heading,
    style_reminder,
)


class SentenceCaseTests(unittest.TestCase):
    def test_converts_title_case(self):
        self.assertEqual(
            sentence_case_heading("Create A New Repository"),
            "Create a new repository",
        )

    def test_keeps_acronyms(self):
        self.assertEqual(
            sentence_case_heading("Configure The REST API Client"),
            "Configure the REST API client",
        )

    def test_leaves_sentence_case_alone(self):
        self.assertEqual(
            sentence_case_heading("Create a new repository"),
            "Create a new repository",
        )


class FormatTests(unittest.TestCase):
    def test_replaces_em_dash(self):
        text = "# Title\n\nThe agent writes the plan — then it formats the doc.\n"
        out = format_markdown(text)
        self.assertNotIn("—", out)
        self.assertTrue("plan, then" in out or "plan. then" in out or "plan. Then" in out)

    def test_preserves_ascii_double_hyphen(self):
        text = "# Title\n\nRun git checkout -- theirs to keep the incoming file.\n"
        out = format_markdown(text)
        self.assertIn("checkout -- theirs", out)
        self.assertNotIn("checkout, theirs", out)
        self.assertNotIn("—", out)

    def test_preserves_double_hyphen_in_inline_code(self):
        text = "# Title\n\nRun `git checkout -- theirs`.\n"
        out = format_markdown(text)
        self.assertIn("`git checkout -- theirs`", out)

    def test_preserves_end_of_options_separator(self):
        text = "# Title\n\nPass flags after -- like npm test -- --coverage.\n"
        out = format_markdown(text)
        self.assertIn("after -- like", out)
        self.assertIn("test -- --coverage", out)

    def test_formats_heading(self):
        text = "# Install The Plugin\n\nDo the thing.\n"
        out = format_markdown(text)
        self.assertIn("# Install the plugin", out)

    def test_skips_fenced_code(self):
        text = "# Title\n\n```md\n# Keep Title Case Here\n```\n"
        out = format_markdown(text)
        self.assertIn("# Keep Title Case Here", out)


class LintTests(unittest.TestCase):
    def test_flags_we_and_passive(self):
        text = "# Guide\n\nWe should install the tool.\nThe file is created by the hook.\n"
        rules = {f.rule for f in lint_markdown(text)}
        self.assertIn("second-person", rules)
        self.assertIn("active-voice", rules)

    def test_flags_missing_h1(self):
        text = "## Section\n\nHello.\n"
        rules = {f.rule for f in lint_markdown(text)}
        self.assertIn("missing-h1", rules)

    def test_flags_weak_opener(self):
        text = "# Guide\n\nSo you run the installer.\n"
        rules = {f.rule for f in lint_markdown(text)}
        self.assertIn("weak-opener", rules)

    def test_does_not_flag_ascii_double_hyphen(self):
        text = "# Guide\n\nRun git checkout -- theirs.\n"
        rules = {f.rule for f in lint_markdown(text)}
        self.assertNotIn("em-dash", rules)

    def test_flags_unicode_em_dash(self):
        text = "# Guide\n\nThe agent writes the plan — then it formats the doc.\n"
        rules = {f.rule for f in lint_markdown(text)}
        self.assertIn("em-dash", rules)


class PathTests(unittest.TestCase):
    def test_doc_paths(self):
        self.assertTrue(is_doc_path("docs/plan.md"))
        self.assertTrue(is_doc_path("README.md"))
        self.assertTrue(is_doc_path("AGENTS.md"))
        self.assertFalse(is_doc_path("src/main.py"))


class HookTests(unittest.TestCase):
    def test_session_start_injects_reminder(self):
        result = run_hook({"hook_event_name": "SessionStart"})
        self.assertIsNotNone(result)
        ctx = result["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Google developer documentation style", ctx)

    def test_pre_tool_use_docs_only(self):
        hit = run_hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": "docs/guide.md"},
            }
        )
        miss = run_hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": "src/app.ts"},
            }
        )
        self.assertIsNotNone(hit)
        self.assertIsNone(miss)

    def test_payload_parse(self):
        self.assertEqual(hook_payload_from_stdin('{"a":1}'), {"a": 1})
        self.assertEqual(hook_payload_from_stdin(""), {})

    def test_reminder_mentions_second_person(self):
        self.assertIn("second person", style_reminder())


if __name__ == "__main__":
    unittest.main()
