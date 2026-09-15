# Selectable behavior patterns

These are proposals to discuss, not defaults to apply indiscriminately. Catalog version: 1.

For each selection, record the pattern ID and version, the user's decision or delegated authority, its concrete scope and parameters, and the checks that prove it. The resolved rule in the goal is authoritative; future library edits do not change accepted goals. Declined or deferred patterns stay outside the required completion contract.

## ACCESS-01 — Sign in before opening a private page

- **Offer when:** a browser page is private.
- **Ask:** “Which pages need sign-in, and where should people go after signing in?”
- **Choose:** return to requested internal page; always go to a named landing page.
- **Resolve:** private route set, login route, public exceptions, return behavior, session-expiry behavior.
- **Check:** signed-out direct navigation reaches login without showing private content; signed-in navigation works; login itself does not redirect in a loop; expiry follows the agreed behavior. If return destinations are supported, reject external/untrusted destinations and test the selected safe fallback.
- **Pair if relevant:** ACCESS-02. A browser redirect alone does not protect data endpoints. API clients usually need a defined unauthorized response rather than HTML navigation.

## ACCESS-02 — Control who can read or change a resource

- **Offer when:** roles, ownership, or shared accounts matter.
- **Ask:** “Who can see this, and who can change it?”
- **Resolve:** actor/resource/action matrix, enforcement boundary, denied response, whether resource existence may be revealed.
- **Check:** allowed action succeeds; denied read and write attempts fail at the server or authoritative boundary; no protected data or mutation leaks. Use two distinct users/workspaces when isolation matters.

## FORM-01 — Help people correct input

- **Offer when:** forms or command inputs can be invalid.
- **Ask:** “Which fields are required, and what should someone see when one needs fixing?”
- **Resolve:** field constraints and boundaries, feedback location, preservation of valid input, server enforcement.
- **Check:** valid boundary values succeed; missing and invalid values produce useful feedback; rejected input creates no unintended record; sensitive fields follow the agreed retention policy.

## SAVE-01 — Recover from a failed save

- **Offer when:** a person edits or creates data.
- **Ask:** “If saving fails, should we keep their work so they can try again?”
- **Resolve:** loading state, retained data, retry action, success indicator, failure simulation.
- **Check:** injected failure shows the chosen recovery action; no false success; retry saves the intended content; refresh persistence matches the agreed promise.

## REPEAT-01 — Prevent accidental duplicate actions

- **Offer when:** duplicate submissions have a meaningful effect.
- **Ask:** “If someone clicks twice or retries, should that count as one action?”
- **Resolve:** duplicate definition and window, retry identity, backend behavior, intentional repeat behavior.
- **Check:** rapid duplicate requests produce the agreed number of effects; a failed request can be retried; a deliberate new action remains possible. Disabling a button alone is insufficient if direct requests can duplicate the effect.

## DELETE-01 — Explain and control removal

- **Offer when:** something can be removed or undone.
- **Ask:** “Should deletion be permanent, recoverable, or require confirmation?”
- **Resolve:** affected objects, permission, confirmation or undo, restoration window, dependent data.
- **Check:** cancel changes nothing; confirmed removal has the agreed scope; denied requests do nothing; recovery works if promised.

## LIST-01 — Define empty, loading, and failure states

- **Offer when:** a screen lists remote or user-created content.
- **Ask:** “What should someone do when this list is empty?”
- **Resolve:** first-use versus no-results messaging, loading indicator, error recovery, filter retention.
- **Check:** distinct empty, filtered-empty, loading, failure, and populated fixtures produce the intended state without stale misleading results.

## NAV-01 — Handle leaving unfinished work

- **Offer when:** people can lose meaningful edits.
- **Ask:** “If they leave before saving, should we warn them or save a draft?”
- **Resolve:** navigation types, draft lifetime and scope, sensitive data limits, discard behavior.
- **Check:** covered navigation preserves or warns as chosen; explicit discard works; saved work does not trigger a false warning.

## A11Y-01 — Complete the journey with a keyboard

- **Offer when:** a web or desktop interface is in scope.
- **Ask:** “Should this whole task be usable without a mouse?”
- **Resolve:** covered journey, visible focus, field labels, errors, dialog focus behavior.
- **Check:** complete the named journey using keyboard only; focus and errors are perceivable; no keyboard trap. This verifies the selected behaviors, not blanket standards compliance.

## DATA-01 — Preserve existing data and callers

- **Offer when:** changing persisted data or an established interface.
- **Ask:** “Who or what depends on the current format?”
- **Resolve:** supported old versions, representative fixtures, migration/backfill, rollback expectation, allowed breaking changes.
- **Check:** old fixtures remain usable as agreed; new and existing callers get the promised results; migration failures follow the recovery plan if migration is in scope.

## EXPORT-01 — Make exported data match expectations

- **Offer when:** exporting reports, tables, or account data.
- **Ask:** “Should the export include what is currently filtered, the current page, or everything you can access?”
- **Resolve:** columns/order, filters, pagination, authorization, empty result, encoding, escaping, filename, consumer expectations.
- **Check:** a known fixture yields the agreed rows and columns; inaccessible data never appears; commas, quotes, and newlines survive parsing. Discuss spreadsheet formula handling when opening untrusted values in spreadsheet software is an expected use case.

## Adding a pattern

Add only patterns with a real use case. Include a stable ID, offer condition, ordinary-language question, meaningful choices, required parameters, positive and negative checks, and relevant interactions. Avoid vendor prescriptions and vague rules such as “make it secure.” An accepted instantiation must be understandable without reopening this catalog.
