# J3012 — snapshot exporter retirement guard

20 November 2026. Continues PR 1011 from 3ab890ae0c; progress remains 3/4.

The board snapshot command was callable outside the guarded publisher. Its watch-link builder can also upload
an internal watch copy and update the local upload register. Added retirement checks to the snapshot command
before parsing/reading channels, and to imported auto_upload before checking credentials, materialising media,
starting the transport or writing its register. The marker is still absent; ordinary behavior is unchanged.

Tests use a real mismatched temporary activation marker and registry. Refusal leaves the output directory absent
and an existing register byte-for-byte intact, with no credential probe, materialisation or transport invocation.
Existing watch tests exercise the unarmed upload paths with fake transport; no real upload was performed.

Validation: 14 engine-guard tests, 35 snapshot tests, 22 watch tests, 13 channel-ratchet tests, eight address-ratchet
tests and five private-network tests pass (97 total). The watch suite's simulated R2 denial is expected coverage,
not an attempted live request. Changed-file scans and whitespace checks run before commit.

No service, marker, credential, film, official daily record or live board was changed. No spend.
Remaining: deployed board Contents access with the actual host credential; direct spend exporters and external
wrapper coverage; MacBook service inventory; refreshed private rehearsal. Seven daily passes, preceding-day
notice and live relay/publish/tick/both-worker acceptance remain prerequisites. Do not restart the runbook or
mark J3012 complete. WW2 has studio/RULES.md but no root AGENTS.md in the current checkout.
