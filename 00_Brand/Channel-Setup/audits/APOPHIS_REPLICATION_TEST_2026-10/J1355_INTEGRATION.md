# J1355 — accepted AR cohort integration, 31 October 2026

Codex covering as elected Chief; authority checked with chief_relay.py status. This is records integration and correction-branch reconciliation, not a new picture PASS or publishing approval.

## Current accepted pairing

| Cut | SHA-256 | Existing acceptance |
|---|---|---|
| AR1 v01 | 49b3e4f0f7276885f942d3451978eba33c9a2fec68216fcafdd79466f877cd07 | J1317, merged PR361 |
| AR2 v06 | 6d517aad6c61a0f12d67b4f2f7990f94ea165e17e01055b56873e89415bf8e67 | J1344, PR371 c70206699 |
| AR3 v05 | 3a2fc5b53e2cfafe4d55422f4f8ae7894ffdb81a727bf47f605e01070a58f13d | J1349 PR373 22175d9db; J1345 confirmation |

Persistent paths are in J1321_CLOSEOUT.json. Version numbers are branch-local; numerically higher does not mean the selected master. Never replace this pairing with AR2 v10/AR3 v09 from the separate earlier correction branch.

## Integrated evidence and historical records

This clean integration preserves the exact file contents from PR370 (7d4f04a17), PR371 (c70206699), PR372 (b5b6be2f0, scoped AR3 correction), PR373 (22175d9db) and PR374 (J1321 close-out 67a26b83c). Their original review and delivery statements remain historical: the AR3 v03 FIX in PR371 is resolved by PR372/373, and old delivery language saying J1321 is held is superseded by the completed close-out. No original report or media manifest is rewritten.

PR363 (worker/J1321-picture-fixes), PR365 (codex/J1324) and PR369 (codex/J1338) form the earlier, separate AR2 v05/v08/v10 and AR3 v09 correction line. J1343 accepted v10 on that line, but J1344/J1349 and the explicit J1321 close-out selected the pairing above. Those PRs are superseded for delivery, not silently merged over the accepted files. Preserve their branches, review decisions and media. J1324 and J1338 are cancelled as superseded correction work, not marked as new PASSes and not reopened for rendering. No unrelated hold is released.

## Next handoff

J1308 is done with the original script/facts/VO/composite-gate decisions; J1317, J1321 and J1345 are done with their respective evidence, correction and picture acceptance records. The queue was searched for existing AR/apophis-replication final-watch work; none existed. Exactly one successor, J1356, depends on J1355. It verifies full moving playback/audio, applicable remaining gates and packaging on these exact masters, then prepares durable per-cut watch paths, hashes and board Play links and sets jobs.py awaits when ready for Ben. It must preserve the existing script/VO lock and explicit test timing exceptions and must not waive a FAIL.

No watch cards are claimed ready by this integration. No upload, schedule, retitle, privacy or Buffer action is authorised by J1355/J1356. Final-watch and publishing gates remain separate; all unrelated date, credit and Ben holds remain. No Ben action is needed for this records job.

## Validation

J1355_INTEGRATION_CHECK.json records fresh matching SHA-256 reads for all eight close-out media/review references (including the three accepted masters and protected AR3 v03), and matching hashes for six raw gate reports. JSON parsing and Python compilation succeeded for the imported files; no media is added to git. Studio core check passed for all 56 shared files; four weekly-public-audit unit tests passed. The saved unmodified gate results and existing WARN rulings are preserved; no fresh render, media-gate rerun, visual review or audio audition is claimed here. GBP0; no media write, NAS deletion or generation.
