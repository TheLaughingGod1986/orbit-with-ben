# J3012: migration branch integration and dry-run process checks

19 November 2026. Continued PR 1011 from 72a231829c. Existing plan remains 3/4.

## Changes

Integrated current main into the existing migration branch in an isolated worktree. Resolved two conflicts:
main's conditional former-resident manifest cache is retained, and the PR's stronger optional-browser-port
assertion is retained, including refusal to dispatch when no port is configured. No channel setting changed.

The split checker previously inspected only parsed unittest failure names. A killed interpreter, startup error
or empty discovery could therefore look like zero failing tests. It now counts an unsuccessful process,
timeout, startup failure, absent success summary or zero-test run as a failed test group. Diagnostic text is
fixed and does not echo process output or exception details. Parsed failures keep their test names.

Updated the runbook with a prominent resume point so the next worker preserves progress and continues the
existing PR instead of recreating the runbook and rehearsal. No official daily-history entry was written.

## Verification

- Split suite: 23 tests pass, including actual subprocess discovery of empty and nonempty fixture suites,
  nonzero and signal exits, missing summaries, timeout/start failures and named failures.
- Queue suite: 67 tests pass; an existing unclosed-file ResourceWarning remains.
- Analytics suite: 46 tests pass.
- Channel ratchet: 13 tests pass; address guard: eight; private-network guard: five.
- Shared core lock check passes (56 files). Resolution/changed-file whitespace checks pass. A whole-merge
  whitespace check also reports existing Markdown line-break spaces in unrelated incoming main files;
  those files are preserved unchanged.

The merged baseline split reported all eight counts zero, routing 2,349 files to studio, 12,856 to Orbit,
60 to History of Science and one to Field Order History, plus one generated status page. This used the existing
baseline identity; it is not a refreshed future-identity remote rehearsal or a daily-history entry.

An explicit full-suite run with the hardened process check initially ran 1,425 tests with one error and
13 skips (exit 1). The local harness had pointed WW2_REPO at an absent ww2-channel scratch folder; the export
uses ww2 from the manifest. The checker correctly rejected this run. That harness setting was corrected;
no channel setting or test expectation was changed to conceal the failure.

The corrected full-suite run passes: 1,425 tests, 13 skips, exit 0. The hardened checker returns no failures.
Logs and exit records are retained locally under J3012-merged-rehearsal-1120 in Mini scratch.
This is a local baseline split verification, not future-identity or live migration acceptance. No service, activation marker, credential,
deployment, channel record or remote studio branch was switched. Nothing was spent.

## Next

Resume the remaining analytics auxiliary gate/dispatch callback, timer/plist integration and isolated fake-API
acceptance described in ANALYTICS_COLLECTION_2026-11-19.md. Then complete the deployed-board Contents probe,
writer inventory/guards and refresh the private rehearsal. Six official full zero days remain recorded through
19 November; seven daily passes and preceding-day notice are still required. Do not mark J3012 done before
the live relay, board publication, harmless tick and both-worker acceptance sequence.
