# J3012 monitor launcher preparation

Continued PR 1011 from 30fa30a8ba; progress remains 3/4.

The tracked missed-run plist fails XML parsing because its comment contains a double hyphen. Reproduced on the
unchanged Git version, then repaired only that comment. The service renderer now prepares this monitor using
literal Python argv, preserving schedule/logs and setting engine/channel roots. A regression parses the actual
template and verifies the proposed arguments, interval, RunAtLoad, logs and source preservation.

The monitor entrypoint checks engine retirement before parsing, fetching, reading or posting. Its boundary test
asserts that neither last_seen nor subprocess runs in a retired engine. Existing engine-guard tests cover actual
marker validation. 33 focused tests and 26 channel/address/private-network tests passed; whitespace check clean.

Remaining monitor blocker discovered: the proposed collector publishes a subject not matched by the existing
tracker check, and moved per-channel record histories need independent monitoring. The runbook explicitly keeps
this monitor out of cutover acceptance until both are adapted and tested. No installed service was repaired or
loaded, and installed versus loaded settings still require reconciliation. No live migration or spend.

Continue board runtime Contents probe, safe HOS guard propagation, monitor record coverage, remaining wrappers,
MacBook inventory and refreshed private rehearsal. Seven official clean days, preceding-day notice and live
relay/board/tick/both-worker acceptance remain required. Existing evidence and progress were retained.
