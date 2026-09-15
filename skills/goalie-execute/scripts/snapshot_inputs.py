#!/usr/bin/env python3
"""Capture or compare explicit local goal/context files; never execute their contents."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys


class Invalid(ValueError):
    pass


def digest(path):
    if not path.is_file():
        raise Invalid(f"Expected a readable file: {path}")
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def located(path, root):
    path = Path(path)
    return Path(os.path.abspath(root / path if not path.is_absolute() else path))


def capture(goal, contexts, root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise Invalid("Project root must be a directory")
    entries, seen = [], set()
    for role, supplied in [("goal", goal)] + [("context", path) for path in contexts]:
        path = located(supplied, root)
        resolved = path.resolve(strict=True)
        if resolved in seen:
            raise Invalid(f"Duplicate input: {supplied}")
        seen.add(resolved)
        try:
            recorded = str(path.relative_to(root))
        except ValueError:
            recorded = str(path)
        entries.append({"role": role, "path": recorded, "sha256": digest(path)})
    return {"format_version": 1, "root": str(root),
            "captured_at": datetime.now(timezone.utc).isoformat(), "inputs": entries}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_manifest(path):
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream, object_pairs_hook=unique_object)


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or set(manifest) != {"format_version", "root", "captured_at", "inputs"}:
        raise Invalid("Invalid input manifest fields")
    if type(manifest["format_version"]) is not int or manifest["format_version"] != 1:
        raise Invalid("Unsupported manifest format_version")
    if not isinstance(manifest["root"], str) or not Path(manifest["root"]).is_absolute():
        raise Invalid("Manifest root must be an absolute path")
    if not isinstance(manifest["captured_at"], str) or not manifest["captured_at"].strip():
        raise Invalid("Manifest needs captured_at")
    entries = manifest["inputs"]
    if not isinstance(entries, list) or not entries:
        raise Invalid("Manifest needs inputs")
    paths, goals = set(), 0
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"role", "path", "sha256"}:
            raise Invalid("Invalid input entry fields")
        if entry["role"] not in ("goal", "context"):
            raise Invalid("Invalid input role")
        goals += entry["role"] == "goal"
        if not isinstance(entry["path"], str) or not entry["path"].strip():
            raise Invalid("Input needs a path")
        if entry["path"] in paths:
            raise Invalid("Duplicate input path")
        paths.add(entry["path"])
        if not isinstance(entry["sha256"], str) or not re.fullmatch(r"[a-f0-9]{64}", entry["sha256"]):
            raise Invalid("Invalid SHA-256")
    if goals != 1:
        raise Invalid("Manifest must contain exactly one goal")


def compare(manifest, root=None):
    validate_manifest(manifest)
    root = Path(root or manifest["root"]).resolve(strict=True)
    if not root.is_dir():
        raise Invalid("Project root must be a directory")
    differences = []
    for entry in manifest["inputs"]:
        path = located(entry["path"], root)
        try:
            current = digest(path)
        except (OSError, Invalid) as exc:
            differences.append(f"Unavailable {entry['role']} {entry['path']}: {exc}")
            continue
        if current != entry["sha256"]:
            differences.append(f"Changed {entry['role']}: {entry['path']}")
    return differences


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("capture", help="Write a new input manifest; refuse overwrite")
    create.add_argument("goal", type=Path)
    create.add_argument("--context", action="append", default=[], type=Path)
    create.add_argument("--root", type=Path, default=Path.cwd())
    create.add_argument("--output", type=Path, required=True)
    check = commands.add_parser("check", help="Report changed or unavailable inputs")
    check.add_argument("manifest", type=Path)
    check.add_argument("--root", type=Path, help="Rebase relative paths to a relocated project")
    args = parser.parse_args(argv)
    try:
        if args.command == "capture":
            manifest = capture(args.goal, args.context, args.root)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(json.dumps(manifest, indent=2) + "\n")
            print(f"Captured {len(manifest['inputs'])} inputs: {args.output}")
        else:
            differences = compare(load_manifest(args.manifest), args.root)
            if differences:
                print("\n".join(differences))
                return 1
            print("Inputs unchanged. This does not validate goal readiness or implementation evidence.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
