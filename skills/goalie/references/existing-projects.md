# Existing projects

The specification describes the intended change and the relevant behavior that must survive it. It does not attempt to reverse-engineer the entire product.

1. Read applicable project instructions and the user's supplied issue, brief, or chat. Locate the affected interface, route, service, data model, and tests. Keep inspection proportional to the change.
2. Record concrete findings with repository-relative paths and, when useful, symbols or line references. Identify the inspected revision or describe the working tree. Distinguish observed implementation, documented intent, and runtime behavior actually tested.
3. Find established run/test commands and relevant baseline results. Run safe, relevant checks if available and authorized; otherwise explain what was not run and why. Do not start services with production side effects just to gather context.
4. Describe the before/after behavior and affected users, callers, or data. Identify contracts to preserve, such as URL behavior, API responses, filters, saved data, or keyboard interaction.
5. Ask only about unresolved decisions. If code and user intent conflict, show the concrete difference. Existing code can contain bugs; it is evidence, not automatic product authority.
6. Turn selected preservation obligations into regression requirements and completion checks. Record known baseline failures precisely. An unrelated known failure may be outside scope if explicitly accepted, but it cannot excuse a new failure or waive a required check.
7. For schema or integration changes, clarify compatibility, migration expectations, test fixtures, and reversibility appropriate to the actual change. Do not add a universal infrastructure programme to small features.

If the repository is unavailable, save a draft with an inspection blocker unless the user has provided enough reliable context to resolve the relevant requirements. Never fabricate file paths, commands, test outcomes, or existing design conventions.

Example finding: “The export button currently sends the selected project ID but ignores the active date filter; `src/reports/export.ts`, function `exportReport`, inspected at revision ….” A corresponding goal might change date filtering while preserving column names relied on by an existing customer import.
