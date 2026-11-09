# J1322 bounded recovery checkpoint — Codex worker, 31 Oct 2026

No Chief approval or film PASS. GBP0. No publishing or NAS overwrite/deletion.

Two exact T1-A old rough duplicates have been removed locally after full SHA-256 readback of both copies, open-file/tracked/symlink/reference checks, stable source checks and durable local/NAS records. Allocated bytes removed: **1,533,317,120 (1.428 GiB)**. See `duplicate_result.json` for full hashes, sizes, absolute paths and df before/after. Before the move (after clean-worktree allocation), df available was 8,780,208 KiB; after it was 10,084,852 KiB (9.618 GiB). Concurrent disk use makes df delta different from unique allocated bytes removed.

Current HOS008 picture is rough v12, per `master_v03/REVIEW_master_v03.md` (J1287), and current/predecessor masters v03/v02 stay local. Current master builders and v11/v12 records do not reference the removed old rough paths. All git records remain. Pointers sit beside each removed MP4 with its `.MOVED_TO_NAS.txt` suffix. Existing NAS duplicates were rehashed in place, never rewritten.

The gain/park/rise diagnostic variants named in T1-A were absent at the proposed existing NAS destinations, so the first batch retained them. The second detached batch copies precisely those three files with rsync to a new unique directory, preserving absolute-path hierarchy, verifies source and destination hashes and stability, writes manifests and per-file pointers, then unlinks only the matching local files. It never takes the master_v01 master or master_v02/v03.

Resume by inspecting these files before doing anything:

- tmux: `J1322-diagnostics`
- log: `/Users/benjaminoats/_desk/jobs/J1322/diagnostics.log`
- completion code: `/Users/benjaminoats/_desk/jobs/J1322/diagnostics.done`
- result, if complete: `/Users/benjaminoats/_desk/jobs/J1322/diagnostic_result.json`
- initial completed batch: `/Users/benjaminoats/_desk/jobs/J1322/recovery.done` = 0
- initial NAS manifest: `/Volumes/data/mac-mini-archive/J1322-20261031-0808-bounded/allowlist.json`
- diagnostic NAS manifest: `/Volumes/data/mac-mini-archive/J1322-20261031-0808-diagnostics/diagnostic_manifest.json`

A missing diagnostic completion marker means still running: do not duplicate it. A present marker must be 0 and the removed ledger/result checked before claiming that batch complete. Studio 027 edit was claimed by codex solely for this move; its prior state was done. Release that claim restoring its prior state when the detached batch has ended. No new film-stage approval is implied.

## Retained candidates and remaining work

`deferred.json` lists 110 exact candidate paths and their individual files, sizes and allocated bytes (4.549 GiB total, not a recovery forecast). It is **not an unlink allowlist**. Before selecting any of these, prove the current and previous scratch, active cut-list/rebuild inputs, watch files and upload/Buffer references individually. In particular:

- T1-B is in a git worktree and is excluded by J1322's explicit worktree prohibition.
- HOS008 code graphics may still be rebuild inputs; retain pending row-level reference proof.
- HOS005/006/007 `_work_` directories need current/predecessor identification and active Shorts-repair dependency checks. A low version or an old timestamp does not clear them.
- Repo-root OWB UAT candidates need canonical full-byte duplicate proof and confirmation that no current watch/reference points at the local path; preserve current/previous versions.
- Apophis candidates need J1321-specific dependency checks and current/previous graphics/assembly retention. AR1 is locked unchanged; AR2/AR3 must remain rebuildable.
- T2-C VO variants need exact current lock evidence and preservation of the current and previous required inputs; not selected this run.

All J1100 inputs/pickups/scratch, OWB027/028 source pools, J1320 inputs, gate cache, iCloud/Desktop/Downloads, application/agent/browser state, rescue folders, launch items and source assets remain untouched. No broad export/home sweep.

The 20 GiB target remains unmet. On next resume, read the diagnostic result and live df, finish dependency checks within the expressly permitted groups, then either continue with a new exact allowlist or provide Chief exact unresolved candidates. Do not broaden automatically. J1100 remains blocked at worker 2/3 under h43-LOOP; only elected Chief may verify >=10 GiB live headroom and reopen it. This checkpoint does not reopen it.
