"""Check this catalog's simple frontmatter, local links, and prompt copies."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PROMPTS = {
    "code-review": "review-prompt.md",
    "test-coverage": "tests-prompt.md",
    "brainstorming": "brainstorming-prompt.md",
}


def main():
    errors = []
    entries = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not entries:
        errors.append("No skills found")
    for entry in entries:
        skill_id = entry.parent.name
        text = entry.read_text()
        header = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_id):
            errors.append(f"{entry.relative_to(ROOT)}: invalid skill ID")
        if not header:
            errors.append(f"{skill_id}: missing frontmatter")
            continue
        # Catalog convention: names and descriptions are single-line scalars.
        for key in ("name", "description"):
            values = re.findall(rf"^{key}:[ \t]*(.+)$", header[1], re.MULTILINE)
            if len(values) != 1 or not values[0].strip().strip("\"'").strip():
                errors.append(f"{skill_id}: expected one nonempty {key}")
            elif key == "name" and values[0].strip().strip("\"'") != skill_id:
                errors.append(f"{skill_id}: name differs from directory ID")
        for link in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (entry.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(entry.parent.resolve()) or not target.exists():
                errors.append(f"{skill_id}: missing or nonportable reference {link}")

    for skill_id, name in PROMPTS.items():
        source = ROOT / "prompts" / name
        reference = ROOT / "skills" / skill_id / "references" / name
        if not source.is_file() or not reference.is_file():
            errors.append(f"{skill_id}: missing source prompt or reference")
        elif source.read_bytes() != reference.read_bytes():
            errors.append(f"{skill_id}: prompt reference drift; run make sync")

    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(f"Checked {len(entries)} skills and {len(PROMPTS)} prompt copies.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
