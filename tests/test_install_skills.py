import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_skills", ROOT / "scripts/install-skills.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallSkillsTest(unittest.TestCase):
    def test_links_complete_skill_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "skills"
            installer.install(destination, ["code-review"])
            target = destination / "code-review"
            inode = target.lstat().st_ino
            installer.install(destination, ["code-review"])
            self.assertEqual(target.resolve(), ROOT / "skills/code-review")
            self.assertEqual(target.lstat().st_ino, inode)
            self.assertTrue((target / "references/review-prompt.md").is_file())

    def test_conflicting_user_content_prevents_the_entire_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            existing = destination / "test-coverage"
            existing.mkdir()
            user_file = existing / "SKILL.md"
            user_file.write_text("User-owned skill\n")
            with self.assertRaises(ValueError):
                installer.install(destination, ["code-review", "test-coverage"])
            self.assertFalse((destination / "code-review").exists())
            self.assertEqual(user_file.read_text(), "User-owned skill\n")

    def test_dangling_symlink_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            target = destination / "code-review"
            target.symlink_to(destination / "unavailable-checkout")
            with self.assertRaises(ValueError):
                installer.install(destination, ["code-review"])
            self.assertEqual(target.readlink(), destination / "unavailable-checkout")

    def test_dry_run_and_invalid_selection_do_not_create_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "skills"
            installer.install(destination, ["code-review"], dry_run=True)
            self.assertFalse(destination.exists())
            for name in ["../prompts", "unknown-skill"]:
                with self.subTest(name=name), self.assertRaises(ValueError):
                    installer.install(destination, ["code-review", name])
                self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
