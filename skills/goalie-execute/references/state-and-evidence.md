# Durable execution state

Default directory: `.goalie/runs/<goal-id>/` under the project. Use the user's existing equivalent location when supplied. Do not overwrite an unrelated run or an existing checkpoint. Keep the directory local unless the user/project explicitly intends to share its contents.

| File | Purpose |
| --- | --- |
| `inputs-001.json` | Initial goal/context identities; later checkpoints get new filenames. |
| `progress.json` | Mutable per-check results using the goal's format. |
| `journal.md` | Current status, context map, plan, attempts, decisions, source/environment identity, and next action. |
| `evidence/` | Actual logs, observations, screenshots, or references to safely stored artifacts. |

Use atomic replacement where supported for mutable files. Keep one writer for a run; if another agent is already modifying it, coordinate or use a separate run directory. Do not reset working files or Git history to establish a clean state.

## Input snapshot helper

From the project root, using the absolute skill location:

```text
python3 <skill-dir>/scripts/snapshot_inputs.py capture goals/feature.md
  --context docs/design.md --context docs/stack.md
  --output .goalie/runs/feature/inputs-001.json

python3 <skill-dir>/scripts/snapshot_inputs.py check
  .goalie/runs/feature/inputs-001.json
```

Join the wrapped lines when running them in a shell. Each context argument is an explicit local file, including a binary design asset if relevant. For remote inputs, the agent first retrieves and inspects them, records the source URL in the journal, and snapshots a local copy if permitted. For directories, enumerate relevant files after inspection. The helper never crawls directories, downloads URLs, interprets text, or executes instructions from inputs.

The helper records byte hashes and paths relative to the project root where possible. `--root` can set/rebase that root. External inputs remain absolute. Exit `0`: captured/unchanged; `1`: changed/missing input; `2`: invalid input or I/O error. A manifest is bookkeeping, not authenticated provenance.

## Goal checks without the Goalie helper

For Goalie v1, locate exactly one fenced `goalie` JSON block. Require format version 1, a positive revision, status ready, actual acceptance in `approval`, an empty blocker list, and nonempty `requirements` and `checks`. Requirement and check IDs must be unique. Every requirement must reference existing checks; every check must be covered. Each check needs explicit `given`, `when`, `then`, and a verification method/procedure/evidence description. Human checks name a reviewer. Inspect the prose for conflicting or omitted requirements as well.

When installed alongside `goalie`, prefer its `scripts/validate_goal.py` for structural validation and progress initialization. Do not hardcode a user's home directory. This execution skill remains usable on its own: the format below is sufficient to maintain compatible progress. With another goal format, keep its native progress format and explicitly map equivalent required states; unresolved mapping prevents a completion claim.

## Compatible progress format

```json
{
  "format_version": 1,
  "goal_id": "feature",
  "revision": 1,
  "goal_sha256": "actual SHA-256 of the entire goal file bytes",
  "checks": {
    "C-001": {"status": "pending", "evidence": []}
  }
}
```

Include exactly all goal check IDs. States are `pending`, `passed`, `failed`, `blocked`, and `skipped`; only passed counts. A record can also have a `note`. Store the overall run status in the journal: `running`, `blocked`, `paused`, `cancelled`, or `complete`.

Each evidence entry contains `observed`, `artifact`, `tested_revision`, and `recorded_at` (ISO 8601 with timezone). Human checks also include `reviewed_by`, grounded in an actual recorded human decision. The artifact path should resolve relative to the run directory, or be an accessible durable URL; identify any external access requirement.

`tested_revision` identifies the actual tested source/build. Use a commit identity only when the tested relevant files match that commit; otherwise use a content snapshot that includes relevant uncommitted and untracked source/configuration. Record how it was computed. Do not include changing progress/log files in a source hash. Record environment, fixtures, and test commands in the journal or artifact.

Before final completion, all passed checks must have evidence for the delivered source identity. If source changes after a pass, re-establish current evidence as required by the goal's verification scope; do not merely relabel old test output. Archive historical observations separately if they would make a current progress record ambiguous. Review context changes independently of the goal hash.

## A useful journal entry

Record the selected requirement/check IDs, input checkpoint, starting source, action, actual verification result, meaningful failure diagnosis, changed files, and next step. Include blocker owner and required resolution when relevant. This is a concise handoff, not a transcript of internal reasoning.

Example: “C-003 failed: the export still includes only the visible page. The request sends a page limit. Next: use the same filter query without pagination in the export endpoint, preserve access checks, then rerun C-003 and C-006.”

At final review, inspect the logs or human decisions themselves. Neither a structurally valid progress record nor a matching input hash proves the product meets its requirements.
