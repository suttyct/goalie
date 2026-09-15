# Why Goalie is shaped this way

Goalie focuses on the agreement an implementation loop needs: what must be true when the work is done. A task list is useful for planning, but completing tasks does not by itself demonstrate that a person's use case works.

## Research and influences

Reviewed on 2026-09-15. These are conceptual influences; Goalie's instructions, examples, and helper are written for this project. There is no bundled upstream implementation or integration dependency.

- [GitHub Spec Kit's clarification workflow](https://github.com/github/spec-kit/blob/main/templates/commands/clarify.md) uses targeted questions to reduce ambiguity and records answers in the specification. Goalie adopts focused clarification and durable answers, while letting the number of questions follow the actual scope.
- [Ralph's PRD skill](https://github.com/snarktank/ralph/blob/main/skills/prd/SKILL.md) emphasizes small stories and verifiable acceptance criteria. Goalie uses concrete outcome checks and keeps implementation planning separate from acceptance. It does not impose a particular browser skill.
- [OpenSpec](https://github.com/Fission-AI/OpenSpec) demonstrates lightweight requirements and scenarios, including changes to existing systems. Goalie captures the relevant baseline and preservation obligations without requiring a specification of the entire legacy system.
- [Cucumber's Gherkin reference](https://cucumber.io/docs/gherkin/reference/) provides a useful distinction between starting conditions, actions, and observable outcomes. Goalie uses those concepts in its check fields; users need not learn Gherkin syntax.

## Decisions

**Conversation before form filling.** Ask about what changes the result. Use concrete recommendations with visible tradeoffs. Keep the technical structure in the file, not in the user's burden of answering.

**One authoritative completion contract.** Prose carries context, decisions, and journeys. The structured block carries the required outcomes and checks. Progress lives separately so the builder cannot confuse its own status notes with the user's requirements.

**All listed requirements matter.** Optional and deferred work sits outside the required contract. There is no required flag that a builder can flip to make a hard check disappear.

**Ready is different from done.** Acceptance and resolved questions make a specification ready. Actual evidence and agreed delivery make implementation complete. The validator checks records, not reality.

**Completion must survive a restart.** Stable IDs, a goal revision, a content hash, and source identities help a resumed loop identify stale work. They are not cryptographic attestations of correct behavior or authenticated approval.

**Stopping does not mean succeeding.** Missing access, human review, repeated failure, and exhausted budgets must produce an honest incomplete result. Goalie does not promise infinite retries will solve every problem.

**Brownfield means a scoped change.** Relevant behavior to preserve becomes a check. Existing implementation is evidence, not proof that its behavior is desired.

## Current limits

- The execution skill runs within an active host session; no background runner or native external-loop adapter is included.
- No automated proof that natural-language requirements are complete or mutually consistent.
- No verification of artifact contents, reviewer identity, actual user acceptance, or supplied build identity by the helper.
- No claim of cross-agent behavioral performance from passing Python tests. Human-led trials and actual skill runs remain necessary.
- No enforcement of a goal's immutability against a hostile writer. The format is designed for cooperative agents with reviewable files.

The next useful improvements should come from real interviews and observed false-completion cases. Add adapters only with a named target format and tests demonstrating that the mapping preserves required behavior and stop conditions.

## Execution and context

The companion `goalie-execute` skill drives implementation using the active agent's existing tools. It preserves the planning/execution distinction while giving users an explicit way to start or resume delivery.

Supporting context has both a meaning and an identity. The journal records whether an input is a required design rule, stack decision, additional requirement, or advisory reference. Input snapshots detect byte changes in relevant local files, including images. Neither hashes nor recorded roles establish authority; the user and applicable instructions determine that.

Additional mandatory outcomes must be reflected in the goal's completion checks. Otherwise an agent could follow the original checklist and miss a requirement added through a supporting document. Conflicts require a recorded resolution, not a hidden precedence guess.

The shared Agent Skills layout supports installation in Codex and Claude Code and use by other compatible hosts. Execution instructions avoid runtime-specific commands. Host capabilities still determine whether a particular project's tests, browser checks, or delivery actions can run.
