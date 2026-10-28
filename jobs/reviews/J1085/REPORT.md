# J1085 — J0961 condition verification, 28 Oct 2026

Codex covering as elected acting Chief. Decision: keep J0961 blocked; the required episode gate still fails. No gate waiver, upload, schedule change, media edit or credit spend.

## Evidence

- J0991 is done. Gemini ruling ea4f1e956 accepts the repaired v04 Shorts, with exact hashes and unchanged Friday/Monday picture.
- J0961 approval history records the three v03 approvals (6411247951, 6411249334, 6411258896), and Claude clearing the Wednesday v04 watch on 28 Oct at 11:16Z after the board OK at 11:13:22Z. Preflight 4619155ea cites Wednesday approval comment 6467508842. No new Ben watch is required by this verification.
- Preflight 4619155ea verifies all three v04 hashes and individual package dry runs / Shorts gates. It explicitly reports the episode gate failure, and says a live slot check remains required before upload.
- Fresh `npm run gate:episode -- --project ../02_Video-Projects/029_Is-Betelgeuse-About-To-Explode` exits 1: subscribe_beat FAIL at 54%, required 25–50%. Script score 92.2/100 passes. Full output is in episode_gate.txt.
- The standing pre-upload rule requires gate:episode PASS. Neither predecessor completion nor the watch approval resolves this failure. No locked script or check was changed to make it pass.

## Next condition

J0961 remains blocked until the required episode gate passes following a separately authorised correction. Preserve accepted v04 hashes and approvals; rerun current upload checks and live slot verification when the job is eventually released. Record an input hold linked to J1085, with the next verification six hours from this check because the previous retry is already past. This verification does not authorise corrective production or an upload.

## Disk prerequisite

Both repositories pulled successfully. Initial OWB pull required sandbox escalation, not repair. Required nas_offload.py --apply completed with exit 1: j0935_wed18_v03 checksum mismatch, local copy kept; 13,122 -> 13,118 MB free. No NAS files deleted. No render started.
