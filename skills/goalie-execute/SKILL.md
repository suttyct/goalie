---
name: goalie-execute
description: Implement an accepted goal file through repeated planning, building, testing, and evidence review. Use when asked to execute, deliver, or resume a goal, with optional design guides, technology choices, and supporting requirements. Runs inside the active coding agent and saves resumable progress; works without agent-specific commands. Use goalie for defining the goal itself.
---

# Goalie Execute

Deliver the user's goal, using the goal file and supplied context as working inputs. Drive the implementation loop yourself with the host's tools. Continue through actionable work without asking permission between routine iterations. Completion requires actual verification of the agreed result.

This is an execution skill, not a background service. It can run in Codex, Claude Code, or another agent that can read instructions, edit files, and execute the required checks. It does not launch another agent, require a specific model, install hooks, or promise to restart a terminated session. Save enough state for any capable agent to resume.

## Start from the supplied inputs

Accept ordinary language, file paths, directories, links, and attachments. The user may provide a goal plus design guidance, a required technology stack, supporting requirements, fixtures, or existing implementation notes. Do not make them use a command-line argument format.

1. Identify the goal and project root. Infer them only when unambiguous. If either is missing, ask for the missing path and inspect available context while waiting; do not start building an invented goal.
2. Read applicable project instructions, the whole goal, and existing run state before edits. Inspect relevant code, tests, and the working tree. Preserve unrelated user work. Use an isolated branch/worktree only when needed by project practice or to avoid interference.
3. Read [context.md](references/context.md), resolve the supporting inputs, and record their purpose and identity. Inspect design images with an image-capable tool; a filename is not evidence that you have understood an image. Use available retrieval tools for links. Record inaccessible sources honestly.
4. Confirm that required behavior, completion checks, and delivery are clear and accepted. For Goalie format v1, require `status: ready`, acceptance, no material blockers, and valid requirement/check links. If the sibling Goalie validator is installed, use it with `--ready`; otherwise perform the checks in [state-and-evidence.md](references/state-and-evidence.md). An invalid or draft goal is not execution-ready. Do not invent acceptance or rewrite its checks to satisfy the validator.
5. Incorporate the user's explicit new constraints before dependent implementation. Follow compatible implementation guidance directly. If supporting requirements add or change required outcomes, update the goal and checks through the goal revision process, preserving IDs and actual acceptance/delegated authority. A new requirement must not live only in a context note where completion checks can miss it. You can perform this revision yourself if Goalie is unavailable.
6. Establish available editing, shell/test, browser, network, and human-review capabilities. Read [host-compatibility.md](references/host-compatibility.md) only when adapting to a host or a missing capability. A missing optional tool need not stop unrelated work; a required check that cannot be performed remains incomplete.

Give a short starting update: goal, material context/stack choices, delivery target, and any unresolved constraint. Ask only questions whose answers affect the work; existing authorization carries forward.

## Establish durable state

Read [state-and-evidence.md](references/state-and-evidence.md). Use `.goalie/runs/<goal-id>/` under the project unless the user has an existing state location. Keep accepted requirements separate from mutable progress. Do not publish or commit private context/evidence by default.

Create an input manifest, a check progress record, and a short journal. The optional `scripts/snapshot_inputs.py` captures/checks local input identities using Python 3.10+, without reading their contents into the journal. If Python is unavailable, record identities with host tools and perform the same comparison manually. Neither helper is mandatory to run this skill.

Do not reset an existing run. On resume, compare the current goal, context, source, and environment with the saved state; inspect actual files and evidence rather than trusting the last status. Preserve the history of failures and changes. Archive superseded checkpoints, invalidate affected evidence, and continue from the next useful action.

## Run the delivery loop

Repeat the following while actionable unmet requirements remain:

1. **Choose a useful slice.** Select a coherent outcome and its required checks, considering dependencies and current failures. Make a short implementation plan. Already-working behavior can be verified rather than rewritten. For a full build, connect real user journeys across components; completing scaffolding is not delivery.
2. **Implement it.** Follow the accepted design, stack, repository conventions, and scope. Make necessary code and supporting configuration changes. Treat suggestions as suggestions and do not add unrelated features. Use the user's supplied examples and fixtures where appropriate.
3. **Verify the behavior.** Run the relevant tests and the check's actual procedure. Include negative paths, preserved behavior, and the user-facing flow. For UI work use available browser/visual checks where required; a successful compile does not demonstrate visual or interactive behavior. When tests fail, diagnose the failure before choosing the next change. Do not weaken assertions to obtain a pass.
4. **Record evidence and remaining work.** Update check states with real observations, artifact locations, source identity, and time. Record what changed, what failed, what was learned, and the next action in the journal. Save before a risky/long action and after each meaningful iteration.
5. **Reassess.** Check for changed inputs and new user instructions. Continue with the next actionable requirement; resolve dependencies where possible. A blocked check does not prevent independent useful work. If the same problem recurs without progress, follow the stop rules below instead of repeating the same action.

Keep the user informed at meaningful milestones, after failures that change the approach, and at the host's expected update frequency. Use ordinary language and identify concrete remaining work. Do not announce completion at the end of an intermediate slice.

## Final verification and delivery

When the required checks appear satisfied:

- Compare the actual result against every required outcome and relevant supporting constraint. Review the diff for unrelated changes, shortcuts, missing integration, and broken preservation requirements.
- Verify the delivered source identity and current input manifest. Run the goal's release/regression checks on that result, with current evidence for all required checks. Inspect the evidence artifacts; do not accept self-reported pass flags as proof.
- Obtain a required human decision from the specified reviewer or an authorized substitute; do not supply it yourself. Where no human review was required, do not introduce one as a new gate.
- Perform the agreed delivery within actual authorization. A local patch, reviewable branch, and deployed application are different outcomes. Do not claim a deployment or external action that was not performed.
- Save the final state and give a concise report: delivered result/location, verification, and any limitation. Report **complete** only when every mandatory check and delivery gate is satisfied. Optional future work does not prevent completion.

## Stop and resume honestly

Respect user/host time, cost, iteration, and permission limits. Never disable the sandbox or expand permissions to keep the loop moving. If the user cancels, save state and stop.

Use an existing host/goal retry policy. If none exists, after three unsuccessful attempts on the same obstacle without new evidence or progress, stop retrying that obstacle, work on independent requirements, then report the blocker. This is a no-progress bound, not a limit of three iterations for an entire build.

When no useful authorized work remains, save **blocked**, **paused**, or **cancelled**, never complete. Name the affected check, what was tried, and the exact missing input or capability. Include a resume instruction pointing to the goal and saved run directory. A host ending the session does not itself indicate completion; the next invocation resumes from durable state.
