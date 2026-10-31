# J1331 — exact UAT paths and bounded headroom

31 Oct 2026, codex. Records-only, GBP0. Films OWB:027, OWB:028. **Proposal: KEEP all 120 exact UAT candidates (767,926,272 allocated bytes); empty recovery allowlist.** No media writes, moves, unlinks, NAS writes/deletes, generation, upload, scheduling or rule changes occurred. This report grants no recovery authority or film PASS.

## Actual serving chain

The main-checkout candidate root is `/Users/benjaminoats/YouTube/orbit-with-ben/OWB UAT`. It is distinct from `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT`. All 120 exact candidate-relative paths have a file at their CloudDocs counterpart at the captured check. Existence checks did not materialise or hash iCloud files.

- `scripts/kanban_snapshot.py:714–716`: default `UAT_DIRS` is CloudDocs, overridable by `OWB_UAT_DIR`. `newest_uat` searches this root and prefers a PHONE copy at its selected version. This is selection code, not evidence that a selected version aired.
- `scripts/kanban_snapshot.py:1011–1030`: `ask_watch` resolves an absolute path literally; a relative path tries **CloudDocs / file**, then **publisher ROOT / file**, then **main checkout / file**. Thus every one of these 120 relative candidate paths currently resolves to its exact CloudDocs counterpart, not its repository-root copy. `candidate_decisions.json` records both absolute paths per file. This statement concerns resolver inputs, not a claim that 120 files each have a board card.
- `scripts/board_publish.py:57–67,281–286`: the publisher runs the snapshot from `~/_desk/scratch/chief/board-wt/owb`, a sparse origin/main worktree whose patterns exclude UAT media. Its ROOT fallback is that worktree; the subsequent explicit main-checkout fallback is different. No worktree UAT was selected or examined.
- The installed `~/Library/LaunchAgents/com.owb.board-publish.plist` runs `python3 "$HOME/YouTube/orbit-with-ben/scripts/board_publish.py" --quiet`; its EnvironmentVariables contain no UAT/root/register overrides. The investigation environment also used defaults. This does not prove no future invoking shell can override them.
- The committed `05_Analytics/kanban/watch_uploads.json` has no 029 Short keys. The local `~/.config/studio-kanban/watch_uploads.json` supplies eight exact relative keys mapping to seven IDs (`watch_registers.json`). CloudDocs-first paths use those relative keys; repository-root fallbacks use an absolute register key instead. A similarly named relative key does not prove a repository-root file was served.
- `stream_link` and `ask_watch` reuse a registered ID or may auto-upload a local selection. **Neither resolver was invoked**, because it can write/upload/materialise. This investigation traced the code and existing records only.
- `sign_watch_url` adds expiry and HMAC over ID/expiry, not a path or media hash. `board_site/api/watch.js` validates that signature/auth, then `r2sign.js:newestWatchUrl` chooses the newest MP4 under `watch/<id>/` in R2 bucket `owb-media`. Playback is an HTTP redirect to that object, never a live read from either local UAT root. `watch_upload.mjs` originally uploads the bytes from its explicit file argument. R2 provenance cannot be established solely from the register key.

### Observed watch collision — separate corrective decision needed

`board_watch_snapshot.json` captures the local published board at 09:44:08Z without signatures or URLs. Wednesday's J0961 approved v04 card names `OWB UAT/029_short_wed09_great_dimming_v04_PHONE.mp4`, while the film watch names Monday's nested v04 PHONE path. **Both resolve to `owb-029-v04`.** The local register confirms both mappings.

Read-only R2 resolution at 09:45:51Z streamed and hashed the newest object for each of the seven existing IDs, without saving media. `r2_resolution.json` records filenames, sizes, complete hashes and ID prefixes; random object keys, URLs and credentials are omitted. The shared ID currently serves **029_short_mon14_half_moon_daylight_v04_PHONE.mp4**, 3,296,201 bytes, SHA-256 `04947ca92e610b6bc6adb49f1ed5cc598a1e6e3607e6e29925b3b4a32496db22`. This means the Wednesday approved card currently plays Monday's cut. It does not establish a YouTube upload fault. No register, board, R2 or media was changed. Chief should commission distinct per-cut watch IDs and verify the corrected cards in a separate job; preserve all sources meanwhile.

## Exact dispositions and reference limits

`candidate_decisions.json` has **120 unique exact paths**, current logical/allocated bytes, symlink checks, CloudDocs counterpart/resolution and a reference-group key into `reference_groups.json` (source filenames and line numbers). All have concrete package-family references; 66 also have exact-basename references (listed separately). A family reference is not misrepresented as an exact physical-copy dependency. The remaining 54 auxiliary/nested copies remain KEEP because their independent redundancy and all exclusions are not cleared, rather than because an indispensable read was proven.

`media_hashes.json` freshly hashes the **24 exact top-level MP4 sources from J1326** and every recorded destination. All 24 source hashes still match J1326 and each has at least one fresh matching NAS copy. NAS is mounted/readable. This is redundancy evidence, not a move approval, and it does not cover all nested media duplicates. All 120 files remain local.

Current/previous and history are distinguished by evidence, not highest version:

- **v04:** J0961's result and approval history explicitly identify the repaired/current watch and uploaded package. UPLOADS records SWDCZfWZVao, k2kEaA7ICjc and heiGCnGKTkE with their exact film export paths and hashes. `upload_buffer_snapshot.json` captures those records and the long's NAS master. Main-checkout UAT is not the recorded upload source, but that alone does not waive current/master exclusions.
- **v03:** J0961 history plus three separate registered v03 IDs establish the preceding watch package. R2 reads return the corresponding three v03 PHONE filenames. Preserve this previous package, including review records.
- **v02:** three separate registered IDs still serve the corresponding v02 PHONE files. `_assemble_029_shorts_v03.py:4–6,47,1120–1135` documents v02 picture/mix reuse for v03. That is a concrete rebuild/history dependency; it does not prove every UAT copy is read directly. Keep pending exact copy-level exclusion clearance.
- **v01:** tracked v01 package/assembly/review records identify these original versions (per-file references). They have no 029 local-register key captured here. Absence from the current register is insufficient proof that all history/rebuild/current-previous exclusions are satisfied. Keep; no claim that v01 aired is made.
- UPLOADS names the three v04 film export sources; the local Buffer manifest has no entries for those three IDs. J0961 records Buffer deferred and J0923 still holds the after-public work. No platform absence is inferred from manifest absence. Queue snapshot preserves relevant live holds and dependencies.

## Two readings and retained scratch

Only the three authorised scratch families were traversed for allocation. Symlink directories were not followed; no broad temp/home/cache/export/iCloud census occurred.

| UTC | Available KiB | GiB free | Short of 20 GiB | Short of 10 GiB |
|---|---:|---:|---:|---:|
| 09:44:43.600977 | 8,881,680 | 8.47023 | 11.52977 | 1.52977 |
| 09:45:03.050832 | 8,879,468 | 8.46812 | 11.53188 | 1.53188 |

`measurements.json` retains raw df and exact per-file allocations at both times. The 2,212 KiB decline is not assigned to a writer. The three families' allocations are identical in both readings and equal J1326's recorded allocations:

| Family | Allocated bytes | Disposition |
|---|---:|---|
| `/private/tmp/J1321-media` | 1,814,634,496 | KEEP: source footage for unresolved AR2 repairs |
| `/private/tmp/J1321-render` | 1,873,313,792 | KEEP: current/previous/trial acceptance unresolved |
| `/private/tmp/J1324-render` | 160,452,608 | KEEP: v08 picture FIX, pending corrected acceptance |

Total **3,848,400,896 bytes (3.58410 GiB)**. J1329's ruling #6541774693 explicitly FIXes late ISS detail despite automated gate passes. The current queue has no completed successor repair acceptance; J1321/J1324 remain blocked. All family files remain KEEP; no version ranking clears them.

## Historical increase: unknown attribution

The brief's 09:02:53 baseline is 5,156,364 KiB (4.91755 GiB); 09:39:07 is 8,952,156 KiB (8.53744 GiB), an increase of **3,795,792 KiB / 3.61995 GiB**. J1326's raw `disk_measurements.json` instead prints **5,156,424 KiB**, a 60 KiB discrepancy versus its report/brief. Using that raw value gives **3,795,732 KiB / 3.61989 GiB**. Preserve both; do not silently correct a historical source.

**Proven byte-attributed recovery in that interval: zero from the inspected records. Entire increase remains unassigned/unknown.** J1322's recorded recovery predates this interval and cannot be counted again. J1326 approved zero bytes. Queue/review commits in the interval record no byte-verified removal accounting for this increase; present allocation/mtime cannot prove what happened then. The three bounded families retain their prior allocations now. No causal attribution to worktree cleanup, APFS, caches, a process exit or any other writer is justified. No sweep was made to fill the gap.

## Handoff

`proposal.json`: empty allowlist, **0 proposed recoverable bytes**. Chief next: review records and the watch-ID collision, then issue any new bounded investigation/allowlist explicitly. This report cannot achieve 20 GiB or authorize J1100 restart. The last measured 8.46812 GiB remains below the required live >=10 GiB Chief verification, and 11.53188 GiB below the house target.

Preserved: J1100 **2/3**, OWB:027/028, h43-LOOP, accepted pickups and every remaining gate; J1320 inputs; HOS008 J1213/J1241 graphic locks; local c0f876ffa and `/private/tmp/J1322-records`; J1322's 3/4 recovery hold. No approval is inferred for picture, UAT, YouTube or spend. No Ben action required for this records handoff. NAS reads succeeded, so no NAS-unavailable retry is needed.
