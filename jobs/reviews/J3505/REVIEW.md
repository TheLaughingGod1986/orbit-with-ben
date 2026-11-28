# J3505 — approved Shorts delivery handoff

Codex covering as elected Chief, 24 November 2026. All five board checks read `ok` for the exact requested version. Their timestamps and source cards are retained in BOARD_APPROVALS.json; no new watch request is required. Approval timestamps are recorded by jobs.py approved to minute precision, as its parser requires; the evidence preserves seconds.

| Cut | Ben approved (16 November, London) | Delivery job | Delivery instruction |
|---|---|---|---|
| Titan Test A v02 | 09:32 | J3508 | New private upload, target 2 December 11:30 |
| Betelgeuse opening v06 | 09:32 | J3510 | Replace scheduled private v04 k2kEaA7ICjc, preserve 11 December 11:30 |
| Betelgeuse half-Moon v06 | 09:13 | J3509 | Replace scheduled private v04 heiGCnGKTkE, preserve 14 December 11:30 |
| HOS 010 Short A v01 | 11:10 | J3512 | Upload private without publishAt now; schedule only after long air date is confirmed |
| HOS 010 Short C v01 | 09:33 | J3511 | Upload private without publishAt now; schedule only after long air date is confirmed |

## Schedule evidence and decisions

The 24 November 06:40Z OWB snapshot lists 27 November (aAUgIGEuPwQ), 28 November (MScK2CK2ZFg) and 30 November (xvarZP2aYyE) as occupied. Therefore 2 December is the first free regular Monday/Wednesday/Friday/Saturday slot after Titan's long T3cBBss1F60 on 25 November 18:00. The upload job must reread live channel state and queued reservations before taking it. No existing slot is moved.

The brief's 8 and 11 December Betelgeuse dates are watch deadlines, not air dates. Source awaits entries, UPLOADS.json and the 24 November snapshot agree on 11 and 14 December at 11:30. UPLOADS.json maps both existing ids to v04; Ben approved v06. Each gets a separate controlled swap job, with an old-private-unscheduled/new-private-scheduled readback required. Parent vP1BbqZ_dnM airs 6 December 18:00. These are future private copies; no permission to duplicate a public idea is given.

The HOS jobs receive no speculative date. They prepare and upload the approved files privately, register the HOS media, and queue scheduling against the confirmed long date and actual long-public state. No Short may air before its long. The pre-19-November approved cuts are preserved; this handoff orders no rebuild.

## Bookkeeping and verification

Five separate Mini-only studio jobs are linked to the exact board cards and approvals, initially dependent on J3505 so no worker starts before the records are ready. Finished assembly J0979 and completed review J2933 are closed with the stale Ben holds removed; they must not be reopened into assembly or another watch.

The current jobs.py approved operation consumes a multi-cut list entry. The final remaining entry loses its original `.1` askId unless retained explicitly. The two `.1` identifiers are therefore preserved in approval metadata, and both original answered request lists retained under awaits_was. Swap job titles include the old video-id `: swap to` form so jobs.py's existing swap readback guard applies.

No YouTube, Buffer, title, privacy or scheduling changes were made in J3505. Dates above are queued instructions, not a claim that a new upload already exists. All upload gates, channel checks, hash checks, privacy and schedule readbacks remain with the delivery jobs. GBP 0 spent.

The Mini had about 9.7 GB free. Required nas_offload --apply ran detached and returned successfully with no eligible scratch to move. Logs: _desk/logs/J3505-scratch.log and .done. No NAS file was deleted.
