# Execute a goal

`goalie-execute` takes an accepted goal and drives repeated implementation and verification in the active agent session. It is intended for Codex, Claude Code, and other agents able to read the portable skill and operate on the project.

## Inputs

Supply the goal path and project location. Add any relevant design guides, stack choices, reference images, acceptance examples, supporting requirements, or links in ordinary language. State which choices are mandatory if that is not already clear.

For example:

```text
Use goalie-execute for goals/report-export.md in this project.
The existing TypeScript stack must stay.
Follow docs/design-system.md for button and error states.
Use docs/export-requirements.md as additional requirements.
The screenshot designs/export.png shows the intended layout.
Deliver the local change and evidence for every required check.
```

The skill reads applicable project instructions first, inspects the goal and code, and resolves the supplied context. It asks only about material gaps. A context document cannot silently add work or weaken accepted requirements; new mandatory behavior must be incorporated into the goal and its checks under the user's actual instructions.

## Execution cycle

1. Read the accepted goal, relevant context, and saved state.
2. Select a useful unmet outcome, accounting for dependencies.
3. Implement within scope and the required stack/design choices.
4. Run the actual acceptance checks and relevant regression checks.
5. Save observations, artifacts, current status, and next action.
6. Continue until every required outcome and delivery gate is verified, or no useful authorized work remains.

The agent performs these steps using its existing tools. There is no `goalie run` executable or CLI adapter in this release. Do not confuse a skill instruction to continue working with a service that can relaunch a dead process.

## Context and evidence across restarts

State lives in `.goalie/runs/<goal-id>/` unless another location is supplied. Keep this local or follow your project's sharing policy; supporting documents and screenshots can contain private information. This repository ignores `.goalie/`, but other projects need their own ignore/sharing decision before committing files.

The optional input helper captures hashes of the goal and explicitly selected local context files. It detects changed or missing inputs. The journal also records the meaning of each source and the mapping to affected requirements. Directory inputs require relevant-file inspection; remote URLs require available retrieval tools and a recorded version or local snapshot when permitted.

On resume, the agent compares inputs and source with the saved state, reads changed material, and invalidates affected results. It does not overwrite an old checkpoint or relabel old test output as current. You can resume in a different capable agent by supplying the goal and run directory; external paths or unavailable tools may need remapping.

## What completion means

Every mandatory check and the agreed delivery target must have current, inspected evidence. Passing the helper proves only that its bookkeeping conditions hold. It does not prove the application works, establish human approval, or inspect screenshots and logs.

Blocked work stays incomplete. Missing credentials, tools, external decisions, and human review are recorded with the exact action needed. The agent still completes independent work where possible. Host time/cost limits apply; repeated failure without progress does not justify an endless retry loop.

## Compatibility and validation

The skill uses the standard `name`/`description` frontmatter and relative resources described by the [Agent Skills specification](https://agentskills.io/specification). It avoids Claude-only frontmatter and Codex-only commands. See [Codex skills](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skills](https://code.claude.com/docs/en/skills) for installation and invocation.

The helper tests exercise changed/missing context, binary assets, relocated roots, symlink changes, duplicate inputs, and refusal to overwrite manifests. These tests do not demonstrate end-to-end model execution. Use the [execution evaluation cases](evaluation.md) for actual host trials.
