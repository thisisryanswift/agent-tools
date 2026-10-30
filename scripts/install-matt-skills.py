"""Install the pinned promoted Matt Pocock pack without replacing user content."""

import argparse
import json
import os
from pathlib import Path
import subprocess


REVISION = "59db609eb1e18aaf59b63284d0e52255aff0c63c"


def promoted_skills(source):
    source = Path(source).expanduser().resolve()
    revision = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    if revision != REVISION:
        raise ValueError(f"Expected upstream revision {REVISION}; found {revision}")
    tracked = [".claude-plugin/plugin.json", "LICENSE", "skills/engineering", "skills/productivity"]
    changed = subprocess.check_output(
        ["git", "-C", str(source), "status", "--porcelain", "--", *tracked], text=True
    )
    if changed:
        raise ValueError("Pinned manifest, license, and promoted skills must be unchanged")
    manifest = json.loads((source / ".claude-plugin/plugin.json").read_text())
    paths = []
    for entry in manifest["skills"]:
        path = (source / entry).resolve()
        if not path.is_relative_to(source / "skills") or not (path / "SKILL.md").is_file():
            raise ValueError(f"Invalid promoted skill path: {entry}")
        paths.append(path)
    if not paths or len({p.name for p in paths}) != len(paths):
        raise ValueError("Promoted skill IDs must be nonempty and unique")
    return paths


def install(paths, destination, dry_run=False):
    destination = Path(destination).expanduser().resolve()
    planned = []
    for source in paths:
        source = Path(source).resolve()
        if destination == source or destination.is_relative_to(source):
            raise ValueError("Destination must be outside the source skill directories")
        target = destination / source.name
        if target.is_symlink() and target.resolve() == source:
            planned.append((source, target, False))
        elif target.exists() or target.is_symlink():
            raise ValueError(f"Existing content at {target}; compare it before replacing")
        else:
            planned.append((source, target, True))
    # Preflight the entire pack before changing the discovery directory.
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
    for source, target, create in planned:
        if create and not dry_run:
            target.symlink_to(source, target_is_directory=True)
        action = "Would link" if create and dry_run else "Linked" if create else "Already linked"
        print(f"{action}: {target} -> {source}")


def main():
    data = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    config = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=data / "agent-tools/upstreams/mattpocock-skills" / REVISION)
    parser.add_argument("--destination", default=config / "opencode/skills")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        install(promoted_skills(args.source), args.destination, args.dry_run)
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
