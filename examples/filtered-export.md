# Export the filtered report

This is a fictional, worked specification, not a claim that a project was inspected or implemented.

## Outcome and scope

A signed-in report viewer can export all rows matching the current filters, across pagination. Existing customers continue to read the same columns. Export customization, scheduled exports, new roles, and report redesign are excluded.

## Starting point

Illustrative repository facts supplied by a fictional fixture: `src/reports/export.ts` exports only the current page; `src/reports/filters.ts` defines date filters as inclusive UTC dates; the existing CSV header is `date,project,amount`; `tests/reports.test.ts` covers viewer access: unauthenticated requests return 401 and disallowed project requests return 403, both without report data. These paths describe a hypothetical project and must be inspected in any real adoption. Baseline in the fictional fixture passes `npm test`; this is not a report of a test run in this repository.

## Journeys and decisions

UC-1: A viewer filters the report and exports it (R-001, R-003, R-004). UC-2: A viewer receives an export error and retries (R-005). Shared ACCESS-02 v1 protects both: only currently authorized rows may leave the server (R-002). Selected EXPORT-01 v1 includes all filtered pages, existing column order, UTF-8, RFC-style double-quote escaping for CSV fields, filename `report.csv`, and a header-only empty export.

Filters use the existing inclusive UTC-date behavior. Dates and amounts retain their current formatting. This export is for a machine import, not a spreadsheet workflow; no formula neutralization is added in this feature. The user accepts that consumer boundary. Preserve current screen pagination and filtering behavior (R-006).

## Verification and delivery

Fixture: project A has 51 authorized matching rows spanning two pages, plus two outside the date range; project B has three inaccessible rows. Include Unicode, commas, quotes, and line breaks in project names. Viewer A can access A only. Use the existing report test command `npm test` in the fictional fixture and add relevant request-level and CSV parsing assertions.

Deliver source and tests in a local branch (R-007); no merge, deployment, or production access. No migration is required. Stop incomplete for missing repository/fixtures or an unavailable test environment, preserve evidence and request what is needed. Whole-feature completion requires every check; passing the export happy path alone is insufficient.

No unresolved decisions within this fictional brief.

## Completion contract

```goalie
{
  "format_version": 1,
  "goal_id": "filtered-export",
  "revision": 1,
  "status": "ready",
  "project_type": "brownfield",
  "scope": "feature",
  "approval": {
    "by": "Fictional example user",
    "basis": "Illustrative acceptance for this example only; not approval for a real build."
  },
  "blockers": [],
  "requirements": [
    {
      "id": "R-001",
      "kind": "use-case",
      "description": "Export all currently filtered rows across pages with inclusive UTC date boundaries.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-001"
      ]
    },
    {
      "id": "R-002",
      "kind": "rule",
      "description": "Only authorized report data can be exported; enforce access on direct requests.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-002",
        "C-003"
      ]
    },
    {
      "id": "R-003",
      "kind": "regression",
      "description": "Preserve existing CSV column names, order, dates, and amount formatting.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-004"
      ]
    },
    {
      "id": "R-004",
      "kind": "rule",
      "description": "Produce UTF-8 report.csv with correctly escaped text and a header-only empty result.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-005",
        "C-006"
      ]
    },
    {
      "id": "R-005",
      "kind": "use-case",
      "description": "Show an actionable export failure and allow retry without losing filters.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-007"
      ]
    },
    {
      "id": "R-006",
      "kind": "regression",
      "description": "Preserve existing screen filtering and pagination behavior.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-008"
      ]
    },
    {
      "id": "R-007",
      "kind": "delivery",
      "description": "Deliver the local branch and passing report/project tests with current evidence.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-009"
      ]
    }
  ],
  "checks": [
    {
      "id": "C-001",
      "given": "Viewer A has a date filter matching 51 A rows across two pages",
      "when": "Export while viewing page 1",
      "then": "CSV contains exactly all 51 matching rows, including both date boundaries; outside dates and B rows are absent.",
      "verification": {
        "method": "automated",
        "procedure": "Request export with active filters; parse CSV and compare row identities against the fixture.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-002",
      "given": "Viewer A cannot access project B",
      "when": "Call the export endpoint directly with project B and mixed A/B identifiers",
      "then": "HTTP 403 is returned and no B content appears.",
      "verification": {
        "method": "automated",
        "procedure": "Exercise direct requests bypassing the UI; assert status and absence of protected payload.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-003",
      "given": "A request has no valid session, including an expired session",
      "when": "Call the export endpoint",
      "then": "HTTP 401 is returned with no report data.",
      "verification": {
        "method": "automated",
        "procedure": "Exercise missing and expired session fixtures at the endpoint.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-004",
      "given": "Existing consumer fixture and known dates/amounts",
      "when": "Export known rows and run the current import parser",
      "then": "Header is date,project,amount in that order; date and amount values match the pre-change fixture and import succeeds.",
      "verification": {
        "method": "automated",
        "procedure": "Compare parsed output with the preserved consumer fixture; run its existing import assertion.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-005",
      "given": "Matching project names contain Unicode, commas, quotes, and newlines",
      "when": "Download and parse the CSV",
      "then": "Filename is report.csv and every parsed text value exactly matches the original UTF-8 text.",
      "verification": {
        "method": "automated",
        "procedure": "Inspect download headers/name and parse with an independent CSV reader.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-006",
      "given": "A valid filter matches zero rows",
      "when": "Export",
      "then": "CSV contains the existing header and zero data rows.",
      "verification": {
        "method": "automated",
        "procedure": "Use an empty fixture and parse the output.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-007",
      "given": "Filters are set and the export endpoint is forced to fail",
      "when": "Export, then restore the endpoint and retry",
      "then": "An error with retry appears; no success download is presented on failure; filters remain and retry yields the selected rows.",
      "verification": {
        "method": "browser",
        "procedure": "Inject one server failure in the browser and inspect state across retry.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-008",
      "given": "The existing report fixture",
      "when": "Change filters and page forward/back after the feature change",
      "then": "Visible rows and pagination match the existing baseline assertions.",
      "verification": {
        "method": "automated",
        "procedure": "Run the existing filtering/pagination tests unchanged, then exercise the browser flow.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-009",
      "given": "The final local branch",
      "when": "Run npm test and the added export scenarios",
      "then": "All required tests pass; source and evidence correspond to the delivered branch content.",
      "verification": {
        "method": "automated",
        "procedure": "Record the full command, exit code, test results, and immutable source identity.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    }
  ]
}
```

## Revision history

- Revision 1: Example scope accepted by the fictional user. No implementation evidence is included.
