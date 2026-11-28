# J3012: Buffer record-root continuation, 19 November

Continued PR #1011 from `0b0991d28b`, preserving the existing step 3 of 4. This is a targeted repair of the
Content Ops failure in `CI_EXECUTION_2026-11-19.md`, not full migration acceptance.

## Change

The engine package location no longer determines Buffer's record/media location after the split. Both existing
social registers stay in Orbit (including `social/hos`). The resident registry continues to resolve its own
checkout. A detached registry requires its explicit absolute checkout environment variable and checks that the
selected manifest is Orbit's, not the engine or another channel. Missing configuration fails before writing.
The engine path remains separate from the content path and local credentials are unchanged.

The same content root feeds profile channel files, ledgers, plans, upload registers, relative package metadata,
media resolution and legacy project scans. Orbit's upload hook now uses it for duplicate checks and registration,
so its new relative records remain readable after the move. Existing Buffer organisation/channel guards remain.

The cutover-only workflow renderer now supplies a SHA-pinned channel checkout and its checkout variable to
Content Ops as well as Rules/Notes. Its regression tests verify the new workflow still runs npm tests and does
not mutate source templates. No active workflow was installed or enabled.

## Observed validation

- Source Content Ops: typecheck and lint exit 0; six desk-lock pretests and **217 application tests pass**.
- Detached future-identity layout: typecheck and lint exit 0; six desk-lock pretests and **217 application tests
  pass**, including the formerly failing real channel-files integration test.
- New tests exercise resident compatibility, missing/relative/wrong-channel checkout refusal, both registers,
  plan/ledger/channel paths, relative media registration/resolution, exact package tags and legacy project scans.
  They use temporary files and make no Buffer, YouTube or media-host requests.
- Workflow renderer: four tests pass in source and detached layout. Detached core lock and rules-copy checks pass.
- Source channel ratchet: 13 tests pass; address guard: eight; private-network guard: five. Diff whitespace and
  changed-file key/address scans pass (zero findings).

The detached check reuses the isolated `J3012-ci-layout-1911` sibling layout from the preceding continuation,
with this change copied into its engine and freshly rendered workflow files. It supplies explicit sibling
checkout variables; no live channel files or services were changed. The prepared channel pin for this local
check is `0b0991d28b3d56fabdf58bd8c1fdd14dae12d137`. This is local macOS validation, not a hosted Ubuntu Actions run.
Initial validation caught a nullable test result and an unused import; both were fixed before the passing runs.

## Still outstanding

The full Python workflow suite has not been rerun here and is not claimed passing. Its WW2 Studio-port assertion
still requires a decision based on the channel's real setup; no port or prelaunch flag was invented. Deployed
board credential Contents access, old-entrypoint single-writer protection, remaining timer adapters and refreshed
private rehearsal export also remain. Run the full fresh split after those repairs. The earlier published
rehearsal is historical, not this commit.

No live identity, credential, service, deployment, social post, YouTube state or daily streak was changed. Five
recorded zero days through 18 November and a missing prior-day notice still prevent cutover. J3012 stays open;
final relay/publish/tick acceptance must happen after the gates hold.
