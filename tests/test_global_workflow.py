"""Exercise the documented tk mapping without touching a real project's tickets."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ManualCritContractTest(unittest.TestCase):
    def test_skill_and_codex_metadata_disable_implicit_invocation(self):
        skill = ROOT / "skills/crit"
        text = (skill / "SKILL.md").read_text()
        header = text.split("---", 2)[1]
        self.assertRegex(header, r"(?m)^disable-model-invocation: true$")
        self.assertIn("allow_implicit_invocation: false", (skill / "agents/openai.yaml").read_text())
        self.assertIn("--host 127.0.0.1 --no-open", text)
        self.assertIn("Only start after an explicit Crit request", text)
        self.assertTrue((skill / "references/protocol.md").is_file())

    def test_hosted_protocol_is_explicit_and_keeps_review_state_isolated(self):
        skill = ROOT / "skills/crit"
        text = (skill / "SKILL.md").read_text()
        self.assertIn("references/hosted.md", text)
        hosted = (skill / "references/hosted.md").read_text()
        self.assertIn("--share-url https://crit.wharfi.sh", hosted)
        self.assertIn('--output "$review_root"', hosted)
        self.assertIn("crit fetch", hosted)
        self.assertIn("not approval", hosted)
        self.assertIn("never fall back to public", hosted)
        self.assertIn("No new comments", hosted)

    def test_current_crit_guidance_uses_the_approved_hosted_target(self):
        paths = [
            "README.md",
            "docs/skill-catalog.md",
            "docs/consolidation-status.md",
            "docs/matt-pocock-rollout.md",
            "docs/global-workflow.md",
            "workflows/matt-workflow.md",
        ]
        stale_phrases = [
            "manually invoked local review",
            "explicitly requested local human review",
            "loopback-by-default protocol",
            "user-established SSH forwarding",
            "no hooks, hosted uploads",
        ]
        for path in paths:
            with self.subTest(path=path):
                text = (ROOT / path).read_text()
                self.assertTrue("https://crit.wharfi.sh" in text, f"{path}: missing hosted target")
                for phrase in stale_phrases:
                    self.assertFalse(phrase in text, f"{path}: stale guidance: {phrase}")


@unittest.skipUnless(shutil.which("tk"), "tk is not installed")
class GlobalTkWorkflowTest(unittest.TestCase):
    def test_spec_children_dependencies_notes_and_completion(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            tickets = root / ".tickets"
            env = dict(os.environ, TICKETS_DIR=str(tickets))

            def tk(*args):
                return subprocess.check_output(
                    ["tk", *args], cwd=root, env=env, text=True, stderr=subprocess.STDOUT
                ).strip()

            spec = tk("create", "Spec: fixture", "-t", "epic", "--tags", "spec", "-d", "Full spec")
            first = tk("create", "First slice", "--parent", spec, "-d", "First criterion")
            second = tk("create", "Second slice", "--parent", spec, "-d", "Second criterion")
            for id in (spec, first, second):
                self.assertRegex(id, r"^[a-zA-Z0-9_-]+$")
                self.assertTrue((tickets / f"{id}.md").is_file())
            tk("dep", second, first)
            self.assertIn(second, tk("blocked"))
            self.assertNotIn(second, tk("ready"))
            self.assertIn("No dependency cycles", tk("dep", "cycle"))
            tk("start", first)
            self.assertIn("status: in_progress", (tickets / f"{first}.md").read_text())
            tk("add-note", first, "Acceptance verified in disposable fixture")
            self.assertIn("Acceptance verified", tk("show", first))
            tk("close", first)
            self.assertIn(second, tk("ready"))
            tk("close", second)
            # Child completion must not silently mark the spec outcome complete.
            self.assertIn("status: open", (tickets / f"{spec}.md").read_text())
            tk("reopen", first)
            self.assertIn("status: open", (tickets / f"{first}.md").read_text())
            self.assertFalse((root / ".scratch").exists())
            self.assertFalse((root / "docs/specs").exists())
            self.assertEqual(len(list(tickets.glob("*.md"))), 3)


if __name__ == "__main__":
    unittest.main()
