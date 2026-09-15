# Choosing the next question

Use this as a map, not a questionnaire. Extract known answers first and ask about the gap most likely to change the result. Keep an internal coverage map of outcome, actors, journeys, rules, scope, constraints, checks, and delivery. Coverage can be “not relevant” with a reason.

## Opening

For “I want a booking app”: “Who is booking what, and what should they be able to finish in the first version?”

For “Add CSV export to the existing dashboard”: inspect the dashboard, filters, access control, and tests, then ask about unresolved export behavior. Do not ask about a new technology stack.

For a detailed brief: summarize the intended result in two or three sentences, identify contradictions, and ask only about consequential gaps. For a supplied chat, distinguish accepted decisions from brainstorms, superseded ideas, and unanswered suggestions.

## Follow a journey

“Walk me through the first thing someone comes here to do.” Then choose relevant follow-ups:

| Gap | Plain question | Useful options |
| --- | --- | --- |
| People and access | Who should be able to do this? | Anyone; signed-in members; a specific role |
| Entry point | Where would they start? | Existing page; new page; direct link |
| Outcome | What should they see when it works? | Saved result; confirmation; next step |
| Persistence | Should it still be there when they return? | This session; this device; their account |
| Empty state | What should someone see before they have added anything? | A clear next action; an explanation; sample data |
| Invalid input | If this information is missing, how should we help them fix it? | Inline message preserving input; guided correction |
| Failure | If saving fails, what should happen to what they typed? | Keep it and retry; save a local draft |
| Repeat action | What if they click twice or retry after a slow response? | Same result once; allow separate intentional actions |
| Concurrent edits | If two people edit this, whose change should win? | Warn about conflict; combine compatible edits; agreed last write |
| Scope | What can wait until later? | Identify specific features from their request |
| Delivery | Where do you want the finished result? | Working locally; reviewable branch; live preview |

Avoid irrelevant risks and universal requirements. A local calculator does not need an authentication interview. A destructive action in a shared workspace does need a clear outcome and permission boundary.

## Suggest without steering silently

Example: “After sign-in, I suggest sending people back to the page they tried to open. It saves them finding it again. Would you prefer that or always opening the dashboard?”

After an answer, record its consequences and move on. If a consequence introduces a new material requirement rather than an established constraint, explain and establish it instead of treating it as already accepted.

Keep selectable bundles small. “For this form, I suggest keeping entered text after a failed save and showing which fields need fixing” is useful. A list of thirty security, analytics, and infrastructure preferences is not.

## Transform loose language

- “Easy to use” → a named person can complete a named task with specified steps or a human review of a concrete flow.
- “Fast search” → dataset, query type, measurement conditions, and a user-selected time target; or a specific perceived delay to remove.
- “Responsive” → supported viewport examples and observable layout behavior, not a claim about every device.
- “Secure” → relevant access, isolation, secret handling, or other specific expectations. Do not claim comprehensive security certification.
- “Like this screenshot” → which layout, interaction, content, and states are required; identify what the image does not show.

When the user does not know, explain the tradeoff, recommend an option, and offer to record an assumption within their delegated authority. Material unresolved behavior keeps the goal in draft. Implementation details that do not change the agreed result can be left to the builder.

## Finish proportionally

A one-line copy change may need one use case and two checks. A complete product needs connected journeys, shared rules, preservation or migration requirements where relevant, and a whole-release gate. Stop interviewing when the outcome and checks are clear; do not keep discovering features merely because the library contains them.
