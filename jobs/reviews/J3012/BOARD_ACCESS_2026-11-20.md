# J3012 board access prerequisite

20 November 2026. Existing PR 1011 and 3/4 plan retained.

## Actual observations

- The initial Cloudflare management read returned 403 with an expired local OAuth session.
- The already installed Wrangler CLI refreshed its existing session successfully. Account output was suppressed.
- A subsequent authenticated read of the studio-kanban project succeeded. Production has BOARD_GH_TOKEN with
  type secret_text, but Cloudflare supplies no value. Preview has no BOARD_GH_TOKEN binding.
- The current production deployment is 9883e7bf-6da5-4a16-b672-ac93e9af4c63.
- No token was printed, extracted into a file, rotated or copied. No deployment or binding was changed.

These observations do not prove whether the deployed GitHub token can read private Studio Contents. The absent
process environment and preview binding cannot substitute for that check. No credential change is requested.

## Concrete next step prepared

Added an opt-in authenticated GET /api/migration handler and Cloudflare route. Disabled by default, fixed target
repository/ref/file, metadata-only result, no anonymous fallback or redirects, bounded upstream calls, no-store,
and sanitized errors. It tests repository privacy, ref access and Contents access using the runtime token.
The runbook now gives deployment, authenticated/anonymous verification, evidence and disable/rollback steps.
This is prepared code, not an installed endpoint or successful live credential probe.

## Validation

Seven probe tests passed, covering disabled/auth/malformed-cookie/open-taps boundaries, method and missing-token
refusal, cookie and key authentication, fixed GET-only destination, pinned file read, private/ref/file validation,
upstream failure with no anonymous retry, sanitized exceptions and no secret/content in responses.
The actual Cloudflare route also refuses disabled and anonymous requests without reaching GitHub.
Existing board data API suite: 25 tests, 21 passed and four browser checks skipped. Board site build suite: four passed.
Board authentication suite: 13 passed. Email ratchet: eight passed; private-network checks: five passed.
The diff whitespace check passed. All checks were offline; none contacted the private repository with the server token.

## Handoff

Deploy only the reviewed additive probe against the current board build, not this entire migration branch; preserve
all production bindings and the rollback deployment. Run it with the actual production credential, record sanitized
results, then disable it. Continue guard installation after draining writers, wrapper and MacBook inventory, and
refreshed rehearsal. Official streak remains six; preceding-day notice and live acceptance remain. No live move,
film change, generation, NAS mutation or spend occurred.
