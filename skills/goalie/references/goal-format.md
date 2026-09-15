# Portable goal format, version 1

A goal is Markdown with exactly one fenced `goalie` block containing JSON. The prose explains intent, context, use cases, decisions, and operating boundaries. The JSON is the authoritative completion contract. Read both; do not let a loop consume only the JSON and miss context or permissions.

Use [the template](../assets/goal-template.md). Keep headings that are useful and remove irrelevant guidance. A tiny feature can be short. Do not duplicate requirements as a separate pass/fail list in prose. Refer to requirement and check IDs instead. If prose and contract conflict, resolve the conflict before execution.

## Contract fields

| Field | Meaning |
| --- | --- |
| `format_version` | Integer `1` |
| `goal_id` | Stable lowercase identifier, e.g. `private-dashboard` |
| `revision` | Positive integer; increment when agreed requirements change |
| `status` | `draft` or `ready`; specification readiness, never implementation completion |
| `project_type` | `greenfield` or `brownfield` |
| `scope` | `full-build` or `feature` |
| `approval` | `null` in an unaccepted draft; otherwise `{by, basis}` with actual user acceptance or delegated authority for this revision |
| `blockers` | Array of unresolved decision descriptions including who can resolve them; empty for ready goals |
| `requirements` | Required outcomes, including shared rules, constraints, preservation, and delivery |
| `checks` | Concrete scenarios that prove the required outcomes |

Each requirement has `id` (`R-001` style), `kind` (`use-case`, `rule`, `constraint`, `regression`, or `delivery`), `description`, `source`, and nonempty `check_ids`. Source identifies the user decision, applicable project constraint, or delegated choice. Optional ideas belong in prose, outside this list. All listed requirements are mandatory. Every check must be referenced by at least one requirement; one check may cover several requirements.

Each check has `id` (`C-001` style), `given`, `when`, `then`, and `verification`:

```json
{
  "id": "C-001",
  "given": "A signed-out browser with no session cookies",
  "when": "It directly opens /dashboard",
  "then": "It reaches /login and no private dashboard content is displayed",
  "verification": {
    "method": "browser",
    "procedure": "Clear cookies, open /dashboard, inspect the final URL and rendered content. Repeat with an expired session.",
    "evidence": "Browser test report or recorded observations including URL, content assertion, and tested source revision"
  }
}
```

Methods: `automated`, `browser`, `manual`, `human`. Automated procedures include commands when known, setup, fixtures, and assertions. Browser/manual procedures must be reproducible. Human checks additionally require `reviewer` identifying the person or role who must decide. Evidence must describe actual results, not merely link to code or tests that have not run.

Use concrete examples and boundary values. Split scenarios when different failures need independent tracking. Do not atomize every click. Use test matrices where the expected result is explicit for every variant.

## Required meaning outside the contract

- Outcome and actors; scope and explicit exclusions.
- Relevant baseline for existing code, or initial state for new builds.
- Journeys and experience decisions with requirement IDs.
- Selected rules with resolved parameters and catalog version where used.
- Verification environment, prerequisites, fixtures, supported platforms, and tool availability.
- Delivery target and actual execution permissions; relevant stop conditions.
- Accepted assumptions, deferred ideas, outstanding decisions, and revision history.

The validator checks JSON structure, IDs, references, blockers, and the presence of acceptance. It does not prove these prose topics are complete, verify that the user really accepted, or judge the adequacy of the checks. That remains part of Goalie's review.

## Drafts

An early draft may have empty requirement/check arrays. Capture missing decisions in `blockers` and do not create fake criteria to satisfy a validator. Ready goals require at least one requirement and check, acceptance, and no blockers. Replace template instructions with actual content before readiness.

## Other loop formats

An adapter must preserve every mandatory outcome, check, evidence requirement, dependency, and human decision. A goal with a blocked check is incomplete even if the target format only provides a boolean `passes`. Preserve richer state in a sidecar if supported, or report the incompatibility. Document and test the mapping; Goalie includes no native Ralph, OpenSpec, or Spec Kit adapter.
