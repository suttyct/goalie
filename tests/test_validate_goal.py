"""Exercise the contract boundaries that could otherwise produce false completion."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/goalie/scripts/validate_goal.py"
SPEC = importlib.util.spec_from_file_location("validate_goal", SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.goal, self.digest = validator.read_goal(ROOT / "examples/daily-list.md")

    def passing_progress(self):
        progress = validator.new_progress(self.goal, self.digest)
        for record in progress["checks"].values():
            record["status"] = "passed"
            record["evidence"] = [{
                "observed": "Synthetic fixture assertion passed; not real product evidence.",
                "artifact": "fixture-report.txt",
                "tested_revision": "synthetic-source-sha256",
                "recorded_at": "2026-09-15T10:00:00+00:00",
            }]
        return progress

    def validate_progress(self, progress):
        return validator.validate_progress(self.goal, self.digest, progress, "synthetic-source-sha256")

    def test_worked_examples_are_ready_contracts(self):
        for path in sorted((ROOT / "examples").glob("*.md")):
            with self.subTest(path=path.name):
                goal, _ = validator.read_goal(path)
                validator.validate_goal(goal, ready=True)

    def test_template_is_a_valid_draft_but_not_ready(self):
        goal, _ = validator.read_goal(ROOT / "skills/goalie/assets/goal-template.md")
        validator.validate_goal(goal)
        with self.assertRaises(validator.Invalid):
            validator.validate_goal(goal, ready=True)

    def test_ready_needs_acceptance_and_resolved_blockers(self):
        for changes in ({"approval": None}, {"blockers": ["User must choose the return page."]},
                        {"requirements": [], "checks": []}, {"status": "draft"}):
            with self.subTest(changes=changes):
                goal = copy.deepcopy(self.goal)
                goal.update(changes)
                with self.assertRaises(validator.Invalid):
                    validator.validate_goal(goal, ready=True)

    def test_duplicate_ids_are_rejected(self):
        for field in ("requirements", "checks"):
            with self.subTest(field=field):
                goal = copy.deepcopy(self.goal)
                goal[field].append(copy.deepcopy(goal[field][0]))
                with self.assertRaises(validator.Invalid):
                    validator.validate_goal(goal)

    def test_missing_dangling_and_orphan_checks_are_rejected(self):
        variants = []
        missing = copy.deepcopy(self.goal)
        missing["requirements"][0]["check_ids"] = []
        variants.append(missing)
        dangling = copy.deepcopy(self.goal)
        dangling["requirements"][0]["check_ids"] = ["C-999"]
        variants.append(dangling)
        orphan = copy.deepcopy(self.goal)
        orphan["requirements"][0]["check_ids"].remove("C-001")
        variants.append(orphan)
        for goal in variants:
            with self.subTest(goal=goal["requirements"][0]):
                with self.assertRaises(validator.Invalid):
                    validator.validate_goal(goal)

    def test_invalid_types_fail_cleanly(self):
        for field, value in (("revision", True), ("format_version", True),
                             ("checks", {}), ("requirements", None), ("approval", "yes"),
                             ("status", ["ready"]), ("goal_id", 123)):
            with self.subTest(field=field):
                goal = copy.deepcopy(self.goal)
                goal[field] = value
                with self.assertRaises(validator.Invalid):
                    validator.validate_goal(goal)

    def test_misspelled_fields_do_not_silently_change_meaning(self):
        self.goal["checks"][0]["verification"]["reviewr"] = "someone"
        with self.assertRaises(validator.Invalid):
            validator.validate_goal(self.goal)

    def test_new_progress_starts_pending(self):
        progress = validator.new_progress(self.goal, self.digest)
        self.assertEqual(len(self.validate_progress(progress)), len(self.goal["checks"]))
        self.assertTrue(all(record["status"] == "pending" and record["evidence"] == []
                            for record in progress["checks"].values()))

    def test_every_nonpass_state_remains_incomplete(self):
        for state in ("pending", "blocked", "failed", "skipped"):
            with self.subTest(state=state):
                progress = self.passing_progress()
                progress["checks"]["C-001"]["status"] = state
                self.assertEqual(self.validate_progress(progress), ["C-001"])

    def test_pass_requires_evidence(self):
        progress = self.passing_progress()
        progress["checks"]["C-001"]["evidence"] = []
        with self.assertRaises(validator.Invalid):
            self.validate_progress(progress)

    def test_changed_goal_or_source_invalidates_evidence(self):
        for field, value in (("goal_sha256", "different"), ("revision", 2), ("goal_id", "another-goal")):
            with self.subTest(field=field):
                progress = self.passing_progress()
                progress[field] = value
                with self.assertRaises(validator.Invalid):
                    self.validate_progress(progress)
        progress = self.passing_progress()
        progress["checks"]["C-001"]["evidence"][0]["tested_revision"] = "old-source"
        with self.assertRaises(validator.Invalid):
            self.validate_progress(progress)

    def test_extra_or_missing_progress_checks_fail(self):
        for extra in (True, False):
            progress = self.passing_progress()
            if extra:
                progress["checks"]["C-999"] = {"status": "pending", "evidence": []}
            else:
                del progress["checks"]["C-001"]
            with self.assertRaises(validator.Invalid):
                self.validate_progress(progress)

    def test_human_check_needs_named_reviewer_and_recorded_review(self):
        check = self.goal["checks"][0]
        check["verification"]["method"] = "human"
        with self.assertRaises(validator.Invalid):
            validator.validate_goal(self.goal)
        check["verification"]["reviewer"] = "Product owner"
        progress = self.passing_progress()
        with self.assertRaises(validator.Invalid):
            self.validate_progress(progress)
        progress["checks"]["C-001"]["evidence"][0]["reviewed_by"] = "Fixture product owner"
        self.assertEqual(self.validate_progress(progress), [])

    def test_evidence_needs_timezone_and_substantive_fields(self):
        for field, value in (("recorded_at", "yesterday"), ("recorded_at", "2026-09-15T10:00:00"),
                             ("observed", "  "), ("artifact", ""), ("tested_revision", None)):
            with self.subTest(field=field, value=value):
                progress = self.passing_progress()
                progress["checks"]["C-001"]["evidence"][0][field] = value
                with self.assertRaises(validator.Invalid):
                    self.validate_progress(progress)

    def test_complete_record_is_distinct_from_proven_correctness(self):
        # The validator deliberately cannot authenticate these synthetic observations.
        self.assertEqual(self.validate_progress(self.passing_progress()), [])

    def test_standard_utc_z_timestamps_are_accepted(self):
        progress = self.passing_progress()
        progress["checks"]["C-001"]["evidence"][0]["recorded_at"] = "2026-09-15T10:00:00Z"
        self.assertEqual(self.validate_progress(progress), [])

    def test_duplicate_json_keys_and_nonstandard_numbers_fail(self):
        for text in ('{"status":"draft","status":"ready"}', '{"value":NaN}', '{"value":Infinity}'):
            with self.assertRaises(validator.Invalid):
                validator.decode(text)

    def test_markdown_fences_are_unambiguous(self):
        block = "```goalie\n" + json.dumps(self.goal) + "\n```\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "goal.md"
            path.write_text("````text\n```goalie\nnot a real contract\n```\n````\n" + block)
            parsed, _ = validator.read_goal(path)
            self.assertEqual(parsed["goal_id"], self.goal["goal_id"])
            for text in (block + block, "no contract", block.removesuffix("```\n")):
                path.write_text(text)
                with self.assertRaises(validator.Invalid):
                    validator.read_goal(path)
            path.write_text(block.replace("```", "~~~"))
            self.assertEqual(validator.read_goal(path)[0]["goal_id"], self.goal["goal_id"])

    def test_cli_initialization_never_overwrites_and_pending_is_nonzero(self):
        with tempfile.TemporaryDirectory() as directory:
            progress = Path(directory) / "progress.json"
            command = [sys.executable, str(SCRIPT), str(ROOT / "examples/daily-list.md")]
            first = subprocess.run(command + ["--init-progress", str(progress)], capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = progress.read_bytes()
            second = subprocess.run(command + ["--init-progress", str(progress)], capture_output=True, text=True)
            self.assertEqual(second.returncode, 2)
            self.assertEqual(progress.read_bytes(), original)
            pending = subprocess.run(command + ["--progress", str(progress), "--tested-revision", "fixture"],
                                     capture_output=True, text=True)
            self.assertEqual(pending.returncode, 1)
            self.assertIn("INCOMPLETE", pending.stdout)

    def test_cli_never_executes_procedure_text(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "should-not-exist"
            self.goal["checks"][0]["verification"]["procedure"] = f"touch {marker}"
            path = Path(directory) / "goal.md"
            path.write_text("```goalie\n" + json.dumps(self.goal) + "\n```\n")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--ready"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
