# Completion and loop handoff

Goalie defines the target. The consuming loop implements and verifies it. Goalie does not launch or schedule a loop, execute commands embedded in a goal, or create an automatic promise of success.

## Readiness and authorization

Read the entire goal and applicable project instructions. Require an accepted, structurally valid `ready` goal. A ready goal establishes intended behavior, not blanket permission to spend money, publish, deploy, access production, or contact others. Capture the actual authorized delivery target in the goal. Existing authorization remains valid within its scope.

The loop must maintain separate mutable progress. Do not add pass flags to the goal, edit requirements to match the implementation, count skipped checks as passed, or treat running out of iterations as success.

## Progress record, version 1

The optional helper creates a JSON progress file with `format_version`, `goal_id`, `revision`, `goal_sha256`, and a `checks` object keyed by every check ID. Each check has `status` and `evidence`. Status is `pending`, `passed`, `failed`, `blocked`, or `skipped`; only `passed` counts toward completion.

Evidence entries contain:

- `observed`: the actual result and how it compares with the expected behavior.
- `artifact`: location of a test log, browser report, captured observation, or human decision record.
- `tested_revision`: immutable build/source identity, including a content identity for uncommitted changes; a branch name alone is not enough.
- `recorded_at`: timestamp with timezone in ISO 8601 format.
- `reviewed_by`: required for human checks; identifies the actual human whose decision is in the artifact.

The helper checks structure, the goal's byte hash, and supplied source identity. It cannot authenticate evidence, inspect artifacts, establish human consent, or prove that a test meaningfully covers the criterion. The loop or reviewer must inspect evidence before claiming completion. Do not place secrets or real user data in evidence artifacts.

Changing any goal bytes invalidates the progress hash. Changing source or the tested environment requires rerunning affected checks; at final review, all required checks must have evidence for the delivered source identity. For simplicity the helper requires that exact identity for every passed check. It does not automatically discover the current source identity.

## Complete means all of the following

1. The accepted revision remains the active goal, with no unresolved material decisions.
2. Every required check, including regression and delivery checks, passed on the delivered result.
3. The evidence is real, available, relevant, and current; required human decisions were made by the specified reviewer or an explicitly authorized substitute.
4. Required project checks pass, and any accepted baseline exclusions are documented without concealing new failures.
5. The agreed delivery artifact exists in its agreed location.

The loop should report completion only after reviewing those conditions. “Evidence record complete” from a helper is necessary bookkeeping, not an independent proof of success.

## Keep working versus stop

Continue while there is an actionable unmet check within scope and meaningful progress is possible. Save what was tried, what changed, and the next action between iterations.

Pause and report an incomplete result when a required decision, credential, unavailable dependency, external action, or human review blocks progress. Identify the exact check and what would unblock it. Retry transient failures with a bounded policy appropriate to the runner; do not spin on an unchanged failure. Respect the host's budgets and retry limits. If the host has none, propose a bounded policy in the goal, such as stopping after three materially different unsuccessful attempts on the same blocker. Stopping is not completion.

For a new requirement or contradiction, revise the goal through Goalie, preserve stable IDs, increment the revision, and obtain acceptance within the user's existing authority. Do not silently shrink scope or reset failed checks to pass.

## Minimal handoff prompt

> Read this goal in full and follow the project's instructions. Work only within the accepted scope and authorized actions. Keep progress and evidence separate from requirements. Implement and verify unmet checks, including the complete user journeys. Report success only after every required check and delivery gate has current, inspected evidence. If blocked or out of budget, preserve progress and report what remains; do not change the goal to manufacture a pass.
