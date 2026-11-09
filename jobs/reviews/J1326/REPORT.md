# J1326 — read-only disk reconciliation, 31 Oct 2026

Worker: codex. Films OWB:027, OWB:028. GBP0. No media moved, copied, unlinked or rewritten; no NAS writes/deletes, generation or publishing. No film approval. J1322 and J1100 remain held; J1100 worker 2/3, h43-LOOP, pickups and all gates preserved. Local c0f876ffa and its /private/tmp/J1322-records worktree remain intact.

## Measured headroom and growth

Two timestamped readings are in disk_measurements.json: 09:01:00 UTC (5,179,280 KiB available) and 09:02:53 UTC (5,156,364 KiB available). The latter is **4.91755 GiB**, **15.08245 GiB short of 20 GiB**, and 5.77145 GiB below J1322's 10.689 GiB readback. Use the raw df fields as authoritative; concurrent allocation means these differences are not recoverable-byte forecasts.

The bounded census measured **7.16161 GiB in /private/tmp**, versus J1318's rounded 1.44 GiB: about **+5.72161 GiB** since that earlier inventory. This is a strong location reconciliation, not an exact attribution of the later J1322 regression. The earlier report has no exact per-file tmp baseline. J1322's available-space reading is later than J1318's; do not equate their timelines.

Largest exact retained growth families now present:

| Exact path | Allocated GiB | Evidence and disposition |
|---|---:|---|
| /private/tmp/J1321-media | 1.690 | crew2.mp4 alone 1.653 GiB. J1321 history records source download and provenance work at 08:10 and NAS-backed source at 08:21. Required J1321/J1324 source: KEEP. |
| /private/tmp/J1321-render | 1.745 | J1321 history records trial v03, revision v04, v05 and AR3 v06/v09 deliveries at 08:14–08:28. Current repair acceptance unresolved: KEEP every version. |
| /private/tmp/owb-J1321 | 0.504 | J1321 history explicitly records worktree creation at 08:10, after c0f876ffa's 08:06:58 commit. Worktree excluded. |
| /private/tmp/J1324-render | 0.149 | J1324 records detached v08 render at 08:53 and delivery at 08:58. Current acceptance unresolved: KEEP. |
| /private/tmp/J1319-wt | 0.500 | Worktree; baseline existence not established, not counted as proven post-J1322 growth. KEEP. |
| /private/tmp/codex-j1317-review | 0.500 | Worktree; baseline existence not established. KEEP. |
| /private/tmp/J1322-records | 0.502 | Contains required preserved local evidence; KEEP. |

The four independently documented J1321/J1324 families total approximately **4.09 GiB**, accounting for much of the later regression. The remaining approximately **1.68 GiB cannot be assigned to exact writers from the available baseline**. Existing other worktrees explain much of the difference from J1318, but their existence at J1322's reading is not proven. No cause is inferred solely from mtime. No home, cache, exports or iCloud sweep was performed.

Every scanned file is owned by benjaminoats. Process snapshot (open_files.json) records PID, parent, user and executable names, with no arguments or secrets. No ffmpeg/rsync process and no writable production file descriptors appeared in that snapshot. Python/tmux/agent processes remain present; lack of an open file is not inactivity proof. Between readings, allocation of all 87,211 original census paths was unchanged; the roughly 22 MiB df decline therefore is not explained by growth of those existing paths. Newly created evidence, files outside this scope, APFS metadata and other writes are not individually apportioned. The large raw census stays local, outside the PR; compact measurements and exact deferred-file decisions are committed.

## Exact retained decisions and current/previous proof

**8,057 deferred files, 4,884,897,792 allocated bytes (4.54905 GiB): KEEP.** file_decisions.csv gives every exact path, current allocation, owner and reason. candidate_decisions.json compares current and prior group allocation. reference_excerpts.json supplies source filenames and line numbers; dependency_snapshot.json records current queue holds. A KEEP is a conservative disposition, not a finding that every byte is indispensable forever.

- HOS005 tied-arm v05 explicitly reads STEMS from _work_s02_tied_arm_v04. Both current v05 and preceding v04 work remain. Valves v03 explicitly reads SRC from _work_s05_valves_v02: both remain. Valves v01 remains an older upload/thumbnail record, even though the newer build pair is v03/v02. Never-saw v04/v03 and sum v04/v03 are retained as current/prior build pairs; original records and pointers remain. Galen v04 and its archived v03 predecessor pointer remain. The v01 blood-pressure, heart-pulse and capillaries folders each have their sole known build's SHORT JSON frame references: KEEP; there is no proven disposable predecessor.
- HOS006's five v01 work folders are their sole recorded build work versions, with direct SHORT JSON frame references. There is no recorded second work version that would make these disposable older scratch. KEEP all five.
- HOS007 smallpox v04/v03 and vacca v05/v04 are preserved build pairs. Earlier smallpox v01 and vacca v02 remain named by original upload manifests and thumbnails. Other earlier work folders are not cleared: their rebuilt source-role is unproven, and version age alone is insufficient. This identifies retained pairs without claiming highest version is what aired.
- Repo-root OWB UAT: all **24 MP4s were SHA-256 checked**, all have an equal-size/hash matching copy; uat_hash_proof.json records full source/destination paths and both full hashes. v04 is the repaired/watch package and v03 the preceding watch record for the 029 Shorts; older v01/v02 include uploaded/history records. Bare relative OWB UAT watch links do not identify whether repo-root or CloudDocs is served. Retain every exact UAT candidate, including auxiliary review files, pending that path resolution and Chief ruling. No worktree UAT was selected or changed. Hash equality is verified redundancy, not clearance of watch/current/previous exclusions.
- HOS008 graphics v01/v02: KEEP pending J1213/J1218 row-level dependency clearance. No new graphics approval inferred.
- Apophis original assembly/graphics families: KEEP while J1321/J1324 acceptance remains open. J1324 v08 and its v05 repair source remain; AR3 v09 and its preceding repair versions remain. No old trial is cleared by the presence of a later number.
- All J1320 and J1100 inputs remain excluded. Durable MOVED_TO_NAS pointers remain KEEP.

## T2-C voice investigation only

Known locks are OWB031 magnetic_field_flip_vo_v02a (Chief h32/J1295), OWB032 titan_landing_vo_v02b (h31/J1294), and HOS013 hos_013_vo_v03a (VO_STATUS.md/J1310). Preserve the corresponding preceding v02, v02a and v03 takes and all locked parts. HOS013's fade_v03a.py accepts IN_v03.wav; its check_v03a.py explicitly compares v03 with the output, proving v03 remains a rebuild/check input. Earlier originals and pickups remain provenance/rebuild sources until separately cleared. No T2-C take is proposed for removal. OWB031's earlier inventory used earth_field_flips_vo as a name; the actual local filenames are magnetic_field_flip_vo. Do not execute that stale inventory as an allowlist.

## Proposal and bounded next decision

**Eligible allowlist: empty; recoverable approved bytes: 0.** proposal.json is explicit. No move or unlink is authorized by this report. Even all 4.54905 GiB of the deferred inventory would yield only about 9.46660 GiB available, leaving **10.53340 GiB** to find for the house floor. It would also fail the 10 GiB J1100 restart threshold. Current 4.91755 GiB is below h43's 6 GiB park threshold.

Bounded next investigation targets are the exact retained J1321-media, J1321-render and J1324-render families above (3.584 GiB combined), **only after picture acceptance resolves their source/current/previous dependencies**. They are not eligible now, and even their entire allocation plus the original inventory would leave approximately 6.95 GiB below 20 GiB. Do not authorize wholesale removal of those families: identify exact disposable files after acceptance. Worktrees are excluded and cannot be counted as proposed recovery. The remaining gap needs a new bounded brief from Chief; broad home/export/cache/iCloud sweeps remain disallowed.

NAS read access worked; real mount and capacity are recorded in uat_hash_proof.json (192.168.1.119:/volume1/data). No external NAS retry hold is needed. Chief next: rule on exact retained dependencies/watch-path serving, authorize a specific file allowlist if warranted, and remeasure headroom before considering J1100. No automatic reopening, PASS or escalation to Ben.
