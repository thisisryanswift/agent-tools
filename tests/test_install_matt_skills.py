import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/install-matt-skills.py"
SPEC = importlib.util.spec_from_file_location("install_matt_skills", SCRIPT)
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallMattSkillsTest(unittest.TestCase):
    def test_conflict_preflights_entire_pack(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            first, second = source / "first", source / "second"
            first.mkdir()
            second.mkdir()
            destination = root / "installed"
            destination.mkdir()
            existing = destination / "second"
            existing.write_text("user content")
            with self.assertRaises(ValueError):
                installer.install([first, second], destination)
            self.assertFalse((destination / "first").exists())
            self.assertEqual(existing.read_text(), "user content")

    def test_dry_run_and_repeat_install(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / "source" / "example"
            skill.mkdir(parents=True)
            destination = root / "installed"
            installer.install([skill], destination, dry_run=True)
            self.assertFalse(destination.exists())
            installer.install([skill], destination)
            installer.install([skill], destination)
            self.assertTrue((destination / "example").is_symlink())
            self.assertEqual((destination / "example").resolve(), skill)

    def test_dangling_foreign_link_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / "example"
            skill.mkdir()
            destination = root / "installed"
            destination.mkdir()
            target = destination / "example"
            target.symlink_to(root / "missing")
            with self.assertRaises(ValueError):
                installer.install([skill], destination)
            self.assertEqual(target.readlink(), root / "missing")

    def test_revision_and_dirty_source_are_rejected(self):
        with patch.object(installer.subprocess, "check_output", return_value="different\n"):
            with self.assertRaisesRegex(ValueError, "Expected upstream revision"):
                installer.promoted_skills("/unused")
        with patch.object(
            installer.subprocess, "check_output", side_effect=[installer.REVISION, " M skills/file"]
        ):
            with self.assertRaisesRegex(ValueError, "must be unchanged"):
                installer.promoted_skills("/unused")


if __name__ == "__main__":
    unittest.main()
