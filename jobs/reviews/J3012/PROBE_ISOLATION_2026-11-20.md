# J3012: probe request isolation

20 November 2026. Continued PR 1011, preserving the existing 3/4 plan.

## Finding and change

The Cloudflare adapter copies string bindings into process.env without removing bindings absent on a later
request. The prepared migration handler read process.env, so a reused runtime could continue probing after
its enable flag was removed, or reuse a removed authentication key or GitHub token. This undermined the
runbook instruction to disable the temporary probe after use.

The migration route now passes its current request bindings directly into the handler. The standalone handler
retains its process.env default for Node usage; the deployed Cloudflare route supplies an explicit environment.
Other board endpoints are unchanged. This is a narrow safeguard for the new temporary endpoint, not a claim
that the adapter's environment handling for every existing endpoint has been audited.

## Validation

The new regression makes four sequential requests in one runtime: enabled, flag removed, board key removed,
and GitHub token removed. Before the fix all four reached the upstream stub (502 each, four calls). After the
fix only the first reaches it; subsequent requests return 404, 401 and 503, respectively. The old route was
restored briefly for the regression and the fixed route restored in a finally block.

- Probe suite: 8 passed, including the regression demonstrated failing before the fix.
- Board data API: 21 passed, 4 browser checks skipped.
- Board authentication: 13 passed.
- Board build: 4 passed.
- Address ratchet: 8 passed; private-network checks: 5 passed.
- Diff whitespace check passed.

All tests were offline. No production deployment, binding, service, activation marker, film, credential or
ledger changed. No spend. Private Contents access remains unverified; these tests do not prove it.

## Continuation

Review and deploy only the additive probe on an otherwise current production board build, as the runbook
specifies; verify real authenticated access and disable it. Neither Studio CDP browser currently had a board
page open during this inspection; no authentication material was printed or extracted. Establish an existing
board authentication path before enabling the probe, so verification and cleanup can complete in one run.
Continue safe HOS guard propagation, wrapper and MacBook inventory, and refreshed private rehearsal.
The official daily history inspected still has six passing days through 19 November. No new row or day-before
notice was claimed. J3012 remains incomplete until its timing gates and live relay/board/tick/worker acceptance.
