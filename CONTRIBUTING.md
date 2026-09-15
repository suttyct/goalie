# Contributing to Goalie

Good changes make the conversation easier or make “finished” less ambiguous. Prefer concrete examples over more universal instructions.

## Change the skill

Keep planning behavior in `skills/goalie/SKILL.md` and execution behavior in `skills/goalie-execute/SKILL.md`; put conditional detail in each skill's references. Preserve short, ordinary-language questions and progressive disclosure. Do not make every user answer questions about authentication, infrastructure, or business metrics.

Both skills should work without agent-specific commands or another installed skill. Keep host-specific installation details separate. Context is part of execution: required design/stack choices must be followed, conflicts resolved, and changed inputs considered before reusing evidence. Do not claim cross-agent execution has been tested unless an actual run supports that claim.

For an interview change, include a realistic starting request and show the behavior it improves. Check the [behavioral evaluation cases](docs/evaluation.md). Do not rely on keyword matching as proof that an agent follows the skill.

## Add a rule

Follow the contribution format at the end of [the rule library](skills/goalie/references/rule-library.md). Include when the rule is relevant, the question a person can answer, material choices, parameters to resolve, and positive/negative checks. A rule is a selectable proposal, not a new default for every goal.

Preserve pattern IDs. Change the catalog version when behavior changes. Previously accepted goals retain their resolved requirements; catalog updates must not silently change them.

## Change the format or validator

Keep the documented contract, template, examples, and validator consistent. Format changes that alter interpretation need a new format version and a migration explanation. Avoid accepting unknown fields silently: an ignored misspelling can hide a completion requirement.

Run `python3 -m unittest discover -s tests -v`. Add behavioral tests for false completion, stale evidence, schema ambiguity, or data loss. The validator must never execute commands from a goal or overwrite a progress record during initialization.

Do not publish real customer requirements, private source, tokens, or production evidence as examples. Use fictional fixtures and label them clearly.
