# Host capabilities and invocation

The skill uses the Agent Skills `SKILL.md` layout and ordinary file/tool instructions. It has no runtime dependency on Codex, Claude, model names, subagents, special hooks, or MCP servers. Actual execution requires a host able to edit the project and perform its checks.

## Codex

Install the `goalie-execute` directory in the configured skills directory. Invoke with `$goalie-execute` and describe the goal, project, and context. Use the current session's tools and permissions. Do not invoke `codex exec` from inside the skill merely to perform the same work again.

## Claude Code

Install the directory as `.claude/skills/goalie-execute` in a project or `~/.claude/skills/goalie-execute` for personal use. Invoke `/goalie-execute` followed by the goal path and context, or use an ordinary-language request that selects the skill. The optional `agents/openai.yaml` is Codex UI metadata; the portable instructions do not depend on it.

## Other agents

Use the host's Agent Skills installation mechanism. If it has none, tell it to read `goalie-execute/SKILL.md` and follow the linked references from that skill directory. Names of file, shell, browser, and question tools differ; choose equivalent capabilities. A chat-only host can explain a plan but cannot claim to have executed a build without project access.

## Capability fallback

- No Python: keep the same durable state and compute file identities with available host tools. Perform structural checks manually and disclose that the helper was not run.
- No browser: use an equivalent available browser capability, or leave required browser/visual checks blocked. Do not substitute a compile check for an interaction check.
- No network: work from available local context; mark required remote inputs/integration verification unavailable.
- No file writes: request an environment with project access; do not claim generated suggestions are an applied patch.
- No human reviewer: complete independent work, preserve pending review, and report incomplete.

A native host continuation/goal mechanism can help if already authorized, but the skill does not require one. It must still use the goal's checks and saved evidence. Automatic restart after process exit requires an external runner or host feature; this skill does not install either. Do not start additional agents or background jobs without applicable authorization.
