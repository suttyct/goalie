# A personal daily list

This is a fictional, worked specification, not a claim that a project was inspected or implemented.

## Outcome and scope

A person can keep a small task list in one browser, mark tasks done, and return later. The entire first release is a single local web page. Accounts, synchronization, multiple lists, due dates, editing, deletion, analytics, and deployment are deferred.

## Starting point

Empty project. The builder may choose the implementation and test runner. This is a browser-local prototype; no backend, external APIs, or credentials are needed. Support current desktop Chromium at 1280 × 800 and a 390 × 844 viewport. Browser storage being cleared intentionally loses the list.

## Use cases and decisions

UC-1: Add the first task and see it in the list (R-001, R-004). UC-2: Mark it done, reopen the page, and later unmark it (R-002, R-003). New tasks appear after existing ones; completed tasks stay in place. Each task is a separate item even when text repeats.

The user selected FORM-01 v1: trim leading/trailing whitespace; allow 1–120 characters after trimming. Rejected input remains editable. SAVE-01 v1: if adding fails, retain input, show a retry action, and do not show an unsaved task as saved. If toggling completion fails, keep the previous completion state and offer retry. A11Y-01 v1 covers both journeys (R-005). There is no login rule because there are no accounts.

## Verification and delivery

Use a fresh browser profile, populated storage, and injected storage failure. The builder creates appropriate automated checks and documents the actual test command once selected; the browser procedures below can verify the contract without a particular runner. Preserve evidence for the delivered source snapshot.

Deliver working local source and start/test instructions (R-006). No public deployment is requested. Milestone 1 is add/validate/recover (R-001, R-004); milestone 2 is persistence and completion (R-002, R-003); milestone 3 is full-journey verification and delivery (R-005, R-006). All three are required for whole-release completion.

No open product decisions. Stop incomplete if the environment cannot run the required browser checks. After three materially different failed attempts on the same environmental blocker, record the attempts and request the missing capability; do not count the checks as passed.

## Completion contract

```goalie
{
  "format_version": 1,
  "goal_id": "daily-list",
  "revision": 1,
  "status": "ready",
  "project_type": "greenfield",
  "scope": "full-build",
  "approval": {
    "by": "Fictional example user",
    "basis": "Illustrative acceptance for this example only; not approval for a real build."
  },
  "blockers": [],
  "requirements": [
    {
      "id": "R-001",
      "kind": "use-case",
      "description": "Add a task with trimmed text between 1 and 120 characters; append it to the list.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-001",
        "C-002"
      ]
    },
    {
      "id": "R-002",
      "kind": "use-case",
      "description": "Toggle completion on and off without moving the task or affecting another task.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-003"
      ]
    },
    {
      "id": "R-003",
      "kind": "use-case",
      "description": "Persist task text, order, and completion in this browser across reload and reopen.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-004"
      ]
    },
    {
      "id": "R-004",
      "kind": "rule",
      "description": "Explain an empty list and allow failed additions or completion changes to be retried without presenting them as saved.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-005",
        "C-006",
        "C-009"
      ]
    },
    {
      "id": "R-005",
      "kind": "constraint",
      "description": "Both journeys work by keyboard at the two supported viewport sizes.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-007"
      ]
    },
    {
      "id": "R-006",
      "kind": "delivery",
      "description": "Deliver runnable local source with reproducible start/test instructions.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-008"
      ]
    }
  ],
  "checks": [
    {
      "id": "C-001",
      "given": "An empty list",
      "when": "Add \"  Buy milk  \", then add \"Buy milk\" again",
      "then": "Two distinct tasks named Buy milk appear in insertion order; input clears after each successful save.",
      "verification": {
        "method": "browser",
        "procedure": "Use the add field and button; inspect both items and cleared input.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-002",
      "given": "The add field is editable",
      "when": "Submit whitespace, 121 characters, one character, and 120 characters in separate trials",
      "then": "Whitespace and 121 characters are rejected with visible explanation and retained input; the valid boundaries each create one task.",
      "verification": {
        "method": "browser",
        "procedure": "Run a parameterized input matrix; compare list length and field value in each trial.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-003",
      "given": "Two tasks exist",
      "when": "Mark the first complete and then unmark it",
      "then": "Only that task changes state, and order remains unchanged.",
      "verification": {
        "method": "browser",
        "procedure": "Exercise the first checkbox twice and assert both tasks after each change.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-004",
      "given": "Two tasks exist and one is complete",
      "when": "Reload and then close/reopen the same page in the same browser profile",
      "then": "Both texts, order, and completion states remain.",
      "verification": {
        "method": "browser",
        "procedure": "Keep origin/profile fixed; compare before and after each navigation.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-005",
      "given": "Fresh browser storage",
      "when": "Open the page",
      "then": "An empty-state explanation and an enabled add field are visible; no sample tasks are silently added.",
      "verification": {
        "method": "browser",
        "procedure": "Clear storage and inspect the first-use page.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-006",
      "given": "Text has been entered and storage writes are forced to fail",
      "when": "Attempt to add, restore storage writes, and retry",
      "then": "Failure preserves the text and shows retry without a saved item; retry creates exactly one stored task.",
      "verification": {
        "method": "browser",
        "procedure": "Inject storage write failure, attempt save, remove failure, retry, and reload.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-007",
      "given": "The page is open at each supported viewport",
      "when": "Complete add, mark, and unmark using only keyboard",
      "then": "Focus is visible, controls have accessible names, every action is reachable, and task text/controls do not overflow the viewport.",
      "verification": {
        "method": "browser",
        "procedure": "Repeat both journeys at 1280x800 and 390x844 with Tab, Shift+Tab, Enter, and Space.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-008",
      "given": "A clean local checkout and documented prerequisites",
      "when": "Follow the supplied start and test instructions",
      "then": "The app starts, the required checks can be reproduced, and the delivered source identity is recorded.",
      "verification": {
        "method": "manual",
        "procedure": "Follow README instructions in a clean directory; capture commands, exit codes, and browser results.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-009",
      "given": "An incomplete task exists and storage writes are forced to fail",
      "when": "Try marking it complete, restore writes, and retry",
      "then": "Failure keeps the task incomplete with an error and retry action; retry marks it complete and that state survives reload.",
      "verification": {
        "method": "browser",
        "procedure": "Inject a storage write failure, toggle the task, inspect the previous state and error, restore writes, retry, and reload.",
        "evidence": "Browser report with actual states before failure, after failure, after retry, and after reload, tied to the tested source identity."
      }
    }
  ]
}
```

## Revision history

- Revision 1: Example scope accepted by the fictional user. No implementation evidence is included.
