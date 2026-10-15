"""Link explicitly selected skills into one execution-host discovery directory."""

import argparse
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def install(destination, names, dry_run=False):
    source_root = (ROOT / "skills").resolve()
    destination = Path(destination).expanduser().resolve()
    if destination == source_root or destination.is_relative_to(source_root):
        raise ValueError("Choose a discovery directory outside the source skills tree")
    if len(names) != len(set(names)):
        raise ValueError("Select each skill only once")

    planned = []
    for name in names:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Invalid skill ID: {name}")
        source = (source_root / name).resolve()
        if source.parent != source_root or not (source / "SKILL.md").is_file():
            raise ValueError(f"Unknown skill: {name}")
        target = destination / name
        if target.is_symlink() and target.resolve() == source:
            planned.append((source, target, False))
        elif target.exists() or target.is_symlink():
            raise ValueError(f"Existing content at {target}; compare and migrate it first")
        else:
            planned.append((source, target, True))

    # Validate the whole selection before creating any links.
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
    for source, target, create in planned:
        if create and not dry_run:
            target.symlink_to(source, target_is_directory=True)
        action = "Would link" if dry_run and create else "Linked" if create else "Already linked"
        print(f"{action}: {target} -> {source}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, help="Skill discovery directory on this host")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("skills", nargs="+", help="Exact IDs from docs/skill-catalog.md")
    args = parser.parse_args()
    try:
        install(args.destination, args.skills, args.dry_run)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
