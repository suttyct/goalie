# Require sign-in for the dashboard

This is a fictional, worked specification, not a claim that a project was inspected or implemented.

## Outcome and scope

Private dashboard content is available only after sign-in. The change adds a guard to an existing dashboard; it does not build sign-up, password reset, a new identity provider, or new roles.

## Starting point

Fictional fixture: `/dashboard` currently renders a summary before checking the session. `/login` and `/help` are public. `/api/dashboard` already returns 401 without a session. Test accounts and an expiry fixture exist. Session revalidation runs before every dashboard data refresh, including the visible Refresh action. In a real project Goalie must inspect these facts and the existing test runner before calling this ready.

## Use cases and chosen rules

UC-1: Signed-out visitor opens `/dashboard` and signs in (R-001). UC-2: Signed-in visitor opens the dashboard (R-002). UC-3: Session expires while viewing it (R-003). The selected ACCESS-01 v1 sends successful sign-in to `/dashboard` every time. Arbitrary return URLs are not supported. `/login` and `/help` remain public. ACCESS-02 v1 preserves server-side protection for `/api/dashboard` (R-004).

## Verification and delivery

Use signed-out, signed-in, and expired-session browser fixtures plus direct HTTP requests. The fictional user wants a local patch and a repeatable browser/request test report (R-005); no deployment. The implementing agent must discover the existing test command from project configuration, not invent one. If the fixture facts or required access cannot be confirmed, return to draft and resolve the discrepancy.

All decisions above are accepted within this fictional example. Pause incomplete when test accounts or browser access are unavailable, and report the blocked checks. Retry transient test setup failures at most three times before asking for the missing capability.

## Completion contract

```goalie
{
  "format_version": 1,
  "goal_id": "private-dashboard",
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
      "kind": "rule",
      "description": "Signed-out visitors to /dashboard reach /login without private content, and successful sign-in opens /dashboard.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-001",
        "C-002"
      ]
    },
    {
      "id": "R-002",
      "kind": "use-case",
      "description": "Signed-in visitors can open the dashboard; public pages remain public.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-003",
        "C-004"
      ]
    },
    {
      "id": "R-003",
      "kind": "rule",
      "description": "On session expiry, remove private dashboard content and send the visitor to /login.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-005"
      ]
    },
    {
      "id": "R-004",
      "kind": "regression",
      "description": "Keep the dashboard API protected independently of browser navigation.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-006"
      ]
    },
    {
      "id": "R-005",
      "kind": "delivery",
      "description": "Deliver the local patch with passing project checks and browser/request evidence.",
      "source": "Fictional user accepted this behavior in the example brief.",
      "check_ids": [
        "C-007"
      ]
    }
  ],
  "checks": [
    {
      "id": "C-001",
      "given": "No session cookies exist",
      "when": "Open /dashboard directly",
      "then": "Final URL is /login; private dashboard content never renders, including during loading.",
      "verification": {
        "method": "browser",
        "procedure": "Observe navigation and rendered states with a delayed session check; assert no private content appears.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-002",
      "given": "The visitor was redirected to /login",
      "when": "Sign in with the valid fixture account",
      "then": "The visitor reaches /dashboard and sees their authorized summary.",
      "verification": {
        "method": "browser",
        "procedure": "Complete existing sign-in and inspect final URL/content; verify no arbitrary return URL is used.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-003",
      "given": "A valid session exists",
      "when": "Open /dashboard directly",
      "then": "Dashboard summary is visible and no login redirect occurs.",
      "verification": {
        "method": "browser",
        "procedure": "Use the signed-in fixture and record navigation/content.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-004",
      "given": "No valid session exists",
      "when": "Open /login and /help separately",
      "then": "Each page remains accessible without a redirect loop or private content.",
      "verification": {
        "method": "browser",
        "procedure": "Inspect navigation and page content for both public routes.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-005",
      "given": "The dashboard is visible with a session that will expire",
      "when": "Expire the session using the fixture, then use the dashboard Refresh action",
      "then": "Private content is removed and navigation ends at /login.",
      "verification": {
        "method": "browser",
        "procedure": "Use the expiry fixture, observe revalidation and the content/URL transition.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-006",
      "given": "No session or an expired session",
      "when": "Request /api/dashboard directly",
      "then": "Response remains 401 without private data.",
      "verification": {
        "method": "automated",
        "procedure": "Run both request fixtures and assert status/body.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    },
    {
      "id": "C-007",
      "given": "The completed local patch",
      "when": "Run discovered project checks and all goal scenarios",
      "then": "Required checks pass and evidence matches the delivered source; no deployment is performed.",
      "verification": {
        "method": "manual",
        "procedure": "Record actual commands from project configuration, exit codes, browser/request results, and source identity.",
        "evidence": "Record the actual assertions/results, fixture, and tested source identity in a report."
      }
    }
  ]
}
```

## Revision history

- Revision 1: Example scope accepted by the fictional user. No implementation evidence is included.
