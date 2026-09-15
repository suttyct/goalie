# Goalie

**Turn an idea into a goal an agent can build and verify.**

Goalie is a skill that walks you through what you want to build, how people should use it, what should happen when things go wrong, and how to tell when the work is finished. It handles a new product, a feature in an existing codebase, or a small change.

You describe the behavior in normal language. Goalie asks focused questions, offers relevant choices, and saves a goal file for your coding agent or agent loop.

> **You:** If someone isn't signed in, send them to login.
>
> **Goalie:** Which pages need sign-in? After they sign in, I suggest returning them to the page they tried to open. Would you prefer that or always opening the dashboard?

The final goal captures the chosen routes and behavior, plus checks for direct links, session expiry, public pages, and protected data where those are relevant. Suggestions become requirements only when accepted or chosen within your delegated authority.

## What you get

- A Markdown goal with context, use cases, experience decisions, boundaries, and a structured completion contract.
- Required checks tied to each outcome, rule, constraint, and delivery expectation.
- For existing projects, a relevant baseline and explicit behavior to preserve.
- A draft you can resume, with open decisions recorded rather than guessed away.
- An optional validator and separate evidence record for loops that adopt this contract.

Goalie defines the work. It does not implement your app, run an autonomous loop, or prove that software is correct merely because a document passes validation. Existing loop formats need an explicit mapping; no native Ralph, OpenSpec, or Spec Kit integration is included.

## Use the skill

The portable skill lives in [`skills/goalie`](skills/goalie). Install that whole directory in your agent's skill directory, including its references, assets, and scripts. For a local Codex installation, copy it into `${CODEX_HOME:-$HOME/.codex}/skills/goalie`. Do not overwrite a locally modified installation without reviewing it.

Then ask:

```text
Use $goalie to help me define the first version of a booking app.
```

```text
Use $goalie to define CSV export for this existing reports page.
Inspect the relevant code and tests before asking me questions.
```

```text
Use $goalie to review goals/private-dashboard.md.
Find unclear behavior and missing completion checks.
```

You can also give an agent the path to [`SKILL.md`](skills/goalie/SKILL.md) directly. Hosts vary in skill discovery and question interfaces. The skill needs no specific connector, network service, or runtime package. The optional helper requires Python 3.10 or later.

## How the conversation works

1. Establish the outcome, people, scope, and whether code already exists.
2. Walk through the important tasks, including relevant failure and recovery paths.
3. Select or adapt useful rules, such as sign-in, permissions, failed saves, or exports.
4. Define concrete checks and the finished delivery artifact.
5. Review the saved draft, resolve material gaps, and record acceptance.

This is an adaptive conversation, not a form with a fixed number of questions. A detailed brief should need fewer questions. A small feature should stay small. Say “you decide” when you want Goalie to make reasonable choices within a stated boundary.

## Goal files and evidence

The default output is `goals/<name>.md`. Its prose explains the project; a fenced `goalie` JSON block lists required outcomes and checks. See the [format reference](skills/goalie/references/goal-format.md) and [template](skills/goalie/assets/goal-template.md).

`draft` and `ready` describe the specification, not the implementation. Readiness needs recorded acceptance and no material open decisions. Implementation evidence belongs in a separate progress file. Every required check must pass; blocked, skipped, failed, and unverified checks remain incomplete.

From this repository root:

```bash
# Check the structure of a ready example.
python3 skills/goalie/scripts/validate_goal.py examples/private-dashboard.md --ready

# Start an evidence record; this refuses to overwrite an existing file.
python3 skills/goalie/scripts/validate_goal.py examples/private-dashboard.md \
  --init-progress /tmp/private-dashboard.progress.json

# Validate a populated record against the source identity actually delivered.
# A newly created record returns 1 because all checks are still pending.
python3 skills/goalie/scripts/validate_goal.py examples/private-dashboard.md \
  --progress /tmp/private-dashboard.progress.json \
  --tested-revision YOUR_IMMUTABLE_SOURCE_ID
```

Exit codes: `0` means the requested structural check passed; `1` means a valid progress record remains incomplete; `2` means invalid input or an I/O error. The helper never runs commands found in goal files. It rejects duplicate IDs, missing check references, stale goal hashes, evidence from a different source identity, and passes without evidence.

**A complete evidence record is not proof of correctness.** The loop must inspect the actual test results, human decisions, and delivered artifact. The validator cannot authenticate observations or user consent. Read the [loop contract](skills/goalie/references/loop-contract.md) before integrating it.

## Worked examples

| Example | What it demonstrates |
| --- | --- |
| [Daily list](examples/daily-list.md) | A complete small greenfield build, browser storage, recovery, and keyboard use |
| [Filtered export](examples/filtered-export.md) | A brownfield feature, filters, permissions, and compatibility |
| [Private dashboard](examples/private-dashboard.md) | Login redirects, session expiry, and server-side access checks |

These are fictional accepted specifications, not completed implementations or reports of real repository inspection.

## Develop and contribute

Run the dependency-free tests:

```bash
python3 -m unittest discover -s tests -v
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for adding rules and evaluating interview behavior. The [design notes](docs/design.md) explain the research behind the approach and the limits of completion checking.

Licensed under the [MIT License](LICENSE).
