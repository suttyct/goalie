# Goal: Name the intended result

## Outcome and scope

Describe who needs this, what they can accomplish, and what this release includes. List explicit exclusions and optional future ideas separately.

## Starting point

For an existing project: record inspected paths/revision, current behavior, relevant test baseline, and what must be preserved. For a new build: describe the initial state and established constraints. Do not invent inspection results.

## Use cases and experience

Describe each meaningful journey: actor, starting state, action, visible result, data effects, and relevant failure/recovery paths. Link to requirement IDs in the completion contract. Include the selected shared rules and resolved parameters, not another pass/fail checklist.

## Decisions and open questions

Record accepted decisions and their source, delegated choices and assumptions, declined/deferred suggestions, and the next question. Material open questions also appear in contract blockers. Record acceptance only when it actually occurred.

## Verification and delivery

Specify environment, fixtures, commands or reproducible procedures, required tools, human reviewers if any, delivery artifact, and actual execution permissions. Include required project checks in the contract. Describe when a blocked loop should stop and ask for help.

## Completion contract

```goalie
{
  "format_version": 1,
  "goal_id": "new-goal",
  "revision": 1,
  "status": "draft",
  "project_type": "greenfield",
  "scope": "feature",
  "approval": null,
  "blockers": ["User: describe the outcome and first use case."],
  "requirements": [],
  "checks": []
}
```

## Revision history

- Revision 1: Initial draft. Record subsequent material changes and the acceptance basis for each revision.
