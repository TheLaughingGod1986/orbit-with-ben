# J3012 — repeatable installed-service inventory

20 November 2026; continues PR 1011 from 4b1c62cc4e. Preserve progress 3/4.

Added `scripts/mini/inventory_services.py`: a read-only, bounded scan of selected installed plist files and
explicit wrapper targets. It emits only safe labels, hashes, statuses and booleans; no command lines, environment
names/values, source text or local paths. It executes nothing. All rows require manual review; lexical mentions
of guards or pauses are expressly not safety proofs. Malformed and missing inputs fail visibly without leaking
exception text or discarding other service rows.

The actual Mini scan read 18 installed definitions: 17 parsed and the missed-runs plist was malformed XML.
The previously unresolved scheduled Cursor launcher expands to the local legacy wrapper. Its prompt still
claims Chief authority for Cursor and its pause check does not check engine retirement. The Grok watchdog has
three independent restart paths and no pause/retirement guard. The runbook now identifies their drain order,
retention, resumption conditions and the separate Grok app launch agent. It also distinguishes the separate
Cursor worker services, browser service, channel desk/reminder and unresolved shell targets.

No installed file was changed. Installed definitions do not prove services are loaded; loaded state and process
children must be checked during the window. The MacBook inventory is still outstanding. The obsolete Cursor
prompt must not be resumed after cutover; retain it for rollback and use the current relay's specialist routing.

Validation: seven inventory tests, nine existing service-renderer tests, 13 channel-ratchet tests, eight address
and five private-network checks pass. Changed-file diff and credential/address checks are recorded at handoff.
No full split run is claimed for this read-only inventory addition.

Next: deployed board Contents probe; remaining wrapper/exporter guards and replacements; MacBook service
inventory; refreshed private rehearsal. Seven daily passes, preceding-day notice and live relay/board/tick/both
worker acceptance remain required. Official history was not modified. No live switch, spend or film changes.
