#!/usr/bin/env python3
"""Validate Goalie contracts and evidence records. Never executes goal content."""

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
import re
import sys


class Invalid(ValueError):
    """A human-readable validation error."""


def require(condition, message):
    if not condition:
        raise Invalid(message)


def object_fields(value, required, optional, where):
    require(isinstance(value, dict), f"{where}: expected an object")
    require(set(required) <= value.keys(), f"{where}: missing {sorted(set(required) - value.keys())}")
    require(value.keys() <= set(required) | set(optional),
            f"{where}: unknown fields {sorted(value.keys() - set(required) - set(optional))}")


def nonempty(value, where):
    require(isinstance(value, str) and bool(value.strip()), f"{where}: expected nonempty text")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"JSON: duplicate key {key!r}")
        result[key] = value
    return result


def decode(text):
    def reject_constant(value):
        raise Invalid(f"JSON: invalid constant {value}")
    try:
        return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except json.JSONDecodeError as exc:
        raise Invalid(f"Invalid JSON: {exc}") from exc


def read_goal(path):
    raw = Path(path).read_bytes()
    # Track all Markdown fences so illustrative nested blocks are not interpreted.
    blocks, active, content = [], None, []
    for line in raw.decode("utf-8").splitlines():
        if active is None:
            match = re.fullmatch(r" {0,3}(`{3,}|~{3,})([^`]*)", line)
            if match:
                fence, language = match.groups()
                active = (fence[0], len(fence), language.strip() == "goalie")
                content = []
        else:
            char, length, is_goal = active
            if re.fullmatch(r" {0,3}" + re.escape(char) + "{" + str(length) + r",}\s*", line):
                if is_goal:
                    blocks.append("\n".join(content))
                active = None
            else:
                content.append(line)
    require(active is None, "Unclosed Markdown fence")
    require(len(blocks) == 1, "Expected exactly one fenced goalie JSON block")
    return decode(blocks[0]), hashlib.sha256(raw).hexdigest()


def validate_goal(goal, ready=False):
    object_fields(goal, ("format_version", "goal_id", "revision", "status", "project_type",
                        "scope", "approval", "blockers", "requirements", "checks"), (), "goal")
    require(type(goal["format_version"]) is int and goal["format_version"] == 1,
            "Unsupported format_version; expected integer 1")
    require(isinstance(goal["goal_id"], str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", goal["goal_id"]),
            "goal_id: use lowercase words separated by hyphens")
    require(type(goal["revision"]) is int and goal["revision"] > 0, "revision: expected positive integer")
    require(goal["status"] in ("draft", "ready"), "status: expected draft or ready")
    require(goal["project_type"] in ("greenfield", "brownfield"), "Invalid project_type")
    require(goal["scope"] in ("full-build", "feature"), "Invalid scope")
    for field in ("blockers", "requirements", "checks"):
        require(isinstance(goal[field], list), f"{field}: expected an array")
    for blocker in goal["blockers"]:
        nonempty(blocker, "blocker")
    if goal["approval"] is not None:
        object_fields(goal["approval"], ("by", "basis"), (), "approval")
        for key, value in goal["approval"].items():
            nonempty(value, f"approval.{key}")
    if ready or goal["status"] == "ready":
        require(goal["status"] == "ready", "Goal is a draft, not ready")
        require(goal["approval"] is not None, "Ready goal needs a recorded acceptance basis")
        require(not goal["blockers"], "Ready goal has unresolved blockers")
        require(goal["requirements"] and goal["checks"], "Ready goal needs requirements and checks")

    check_ids = set()
    for check in goal["checks"]:
        object_fields(check, ("id", "given", "when", "then", "verification"), (), "check")
        for key in ("id", "given", "when", "then"):
            nonempty(check[key], f"check.{key}")
        cid = check["id"]
        require(re.fullmatch(r"C-[0-9]{3,}", cid), f"Invalid check ID {cid}")
        require(cid not in check_ids, f"Duplicate check ID {cid}")
        check_ids.add(cid)
        verification = check["verification"]
        object_fields(verification, ("method", "procedure", "evidence"), ("reviewer",), cid)
        require(verification["method"] in ("automated", "browser", "manual", "human"),
                f"{cid}: invalid verification method")
        for key in ("procedure", "evidence"):
            nonempty(verification[key], f"{cid}.{key}")
        if verification["method"] == "human" or "reviewer" in verification:
            nonempty(verification.get("reviewer"), f"{cid}.reviewer")

    requirement_ids, used = set(), set()
    for requirement in goal["requirements"]:
        object_fields(requirement, ("id", "kind", "description", "source", "check_ids"), (), "requirement")
        for key in ("id", "description", "source"):
            nonempty(requirement[key], f"requirement.{key}")
        rid = requirement["id"]
        require(re.fullmatch(r"R-[0-9]{3,}", rid), f"Invalid requirement ID {rid}")
        require(rid not in requirement_ids, f"Duplicate requirement ID {rid}")
        requirement_ids.add(rid)
        require(requirement["kind"] in ("use-case", "rule", "constraint", "regression", "delivery"),
                f"{rid}: invalid requirement kind")
        refs = requirement["check_ids"]
        require(isinstance(refs, list) and refs, f"{rid}: needs at least one check")
        require(all(isinstance(ref, str) for ref in refs), f"{rid}: check IDs must be strings")
        require(len(set(refs)) == len(refs), f"{rid}: duplicate check references")
        require(set(refs) <= check_ids, f"{rid}: unknown checks {sorted(set(refs) - check_ids)}")
        used.update(refs)
    require(used == check_ids, f"Checks without a requirement: {sorted(check_ids - used)}")
    return goal


def new_progress(goal, digest):
    validate_goal(goal, ready=True)
    return {"format_version": 1, "goal_id": goal["goal_id"], "revision": goal["revision"],
            "goal_sha256": digest,
            "checks": {check["id"]: {"status": "pending", "evidence": []} for check in goal["checks"]}}


def validate_progress(goal, digest, progress, tested_revision):
    validate_goal(goal, ready=True)
    nonempty(tested_revision, "tested_revision")
    object_fields(progress, ("format_version", "goal_id", "revision", "goal_sha256", "checks"), (), "progress")
    require(type(progress["format_version"]) is int and progress["format_version"] == 1,
            "Invalid progress format_version")
    require(type(progress["revision"]) is int, "Invalid progress revision")
    for key in ("goal_id", "revision"):
        require(progress[key] == goal[key], f"Progress {key} does not match goal")
    require(progress["goal_sha256"] == digest, "Progress is stale: goal contents changed")
    require(isinstance(progress["checks"], dict), "progress.checks: expected an object")
    require(set(progress["checks"]) == {check["id"] for check in goal["checks"]},
            "Progress must contain exactly the goal's check IDs")
    remaining = []
    for check in goal["checks"]:
        cid = check["id"]
        record = progress["checks"][cid]
        object_fields(record, ("status", "evidence"), ("note",), cid)
        require(record["status"] in ("pending", "passed", "failed", "blocked", "skipped"),
                f"{cid}: invalid progress status")
        require(isinstance(record["evidence"], list), f"{cid}: evidence must be an array")
        if "note" in record:
            nonempty(record["note"], f"{cid}.note")
        if record["status"] != "passed":
            remaining.append(cid)
        else:
            require(record["evidence"], f"{cid}: passed without evidence")
        for evidence in record["evidence"]:
            object_fields(evidence, ("observed", "artifact", "tested_revision", "recorded_at"),
                          ("reviewed_by",), f"{cid}.evidence")
            for key in ("observed", "artifact", "tested_revision", "recorded_at"):
                nonempty(evidence[key], f"{cid}.evidence.{key}")
            try:
                # Python 3.10 needs the numeric equivalent of the standard UTC Z suffix.
                timestamp = datetime.fromisoformat(evidence["recorded_at"].removesuffix("Z")
                                                   + ("+00:00" if evidence["recorded_at"].endswith("Z") else ""))
                require(timestamp.tzinfo is not None, f"{cid}: timestamp needs a timezone")
            except ValueError as exc:
                raise Invalid(f"{cid}: invalid evidence timestamp") from exc
            if record["status"] == "passed":
                require(evidence["tested_revision"] == tested_revision,
                        f"{cid}: evidence is for a different source revision")
                if check["verification"]["method"] == "human":
                    nonempty(evidence.get("reviewed_by"), f"{cid}.reviewed_by")
    return remaining


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("goal", type=Path)
    parser.add_argument("--ready", action="store_true", help="Require an accepted ready goal")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--init-progress", type=Path, help="Create a pending progress file; refuses overwrite")
    modes.add_argument("--progress", type=Path, help="Validate evidence bookkeeping; requires --tested-revision")
    parser.add_argument("--tested-revision", help="Exact immutable identity of the delivered source/build")
    args = parser.parse_args(argv)
    if bool(args.progress) != bool(args.tested_revision):
        parser.error("--progress and --tested-revision must be used together")
    try:
        goal, digest = read_goal(args.goal)
        validate_goal(goal, ready=args.ready)
        if args.init_progress:
            progress = new_progress(goal, digest)
            with args.init_progress.open("x", encoding="utf-8") as output:
                output.write(json.dumps(progress, indent=2) + "\n")
            print(f"Created pending progress: {args.init_progress}")
        elif args.progress:
            progress = decode(args.progress.read_text(encoding="utf-8"))
            remaining = validate_progress(goal, digest, progress, args.tested_revision)
            if remaining:
                print("INCOMPLETE: " + ", ".join(remaining))
                return 1
            print("EVIDENCE RECORD COMPLETE. Inspect actual evidence and delivery before declaring success.")
        else:
            print(f"VALID {goal['status']} contract. This checks structure, not product correctness or user consent.")
        return 0
    except (Invalid, OSError, UnicodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
