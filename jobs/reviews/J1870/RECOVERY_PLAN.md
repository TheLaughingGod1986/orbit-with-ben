# J1870 — live Buffer audit and proposed recovery

Codex covering, authenticated Mac mini, 3 November 2026, 18:22–18:30 UTC. **Audit complete; recovery has not run.** No Buffer post, media-host object, YouTube state/date, credential, or scheduler configuration changed. Both repositories pulled current. No secrets in evidence. Clean report worktree: `codex/J1870-buffer-audit`.

## What is actually queued

Complete authenticated GraphQL enumeration: OWB 218 posts over three pages, HOS 64 over one page; final `hasNextPage=false` for both. All six configured channels match the correct organization, connected, unlocked and queue unpaused. YouTube tokens independently identify `UC_esArsDKd3GJvOkeO0DUog` and `UCXp7HkBIl1LgaznXuZHJyRg`. Profile/org/network ids are in `*-live-summary.json`; every current ledger receipt is joined to its live status in `*-receipts.json`. None of those receipts is missing from the live listing.

| Profile/network | Scheduled | Sent in complete listing | Error |
|---|---:|---:|---:|
| OWB Instagram | 1 | 72 | 0 |
| OWB Facebook | 1 | 73 | 0 |
| OWB Threads | 1 | 70 | 0 |
| HOS Instagram | 4 | 17 | 0 |
| HOS Facebook | 4 | 17 | 1 |
| HOS TikTok | 4 | 17 | 0 |

Ben's widget is correct for OWB; HOS is a separate org. Free-plan capacity is 10 scheduled per channel: OWB has nine free slots, HOS six. No upgrade needed. OWB TikTok stays excluded; HOS TikTok remains authorized through its own Buffer org only.

OWB's existing scheduled item is `T9fVlG3CCzU`, 7 Nov 11:30Z: Instagram `6ae5e281a114574349a5d8ef`, Facebook `6ae5e282b84259308bd83f33`, Threads `6ae5e283a114574349a5d990`. All are scheduled, with 1080×1920 video metadata and processing/transcoding false. Keep them.

HOS's four items (each IG/FB/TikTok):

| Video | Due UTC | Instagram / Facebook / TikTok post ids |
|---|---|---|
| `c2q7w0pgcn8` | 4 Nov 11:30 | `6ae330bca0a200dca8ba6c41` / `6ae330bd6b2f54fd8538e97f` / `6ae330beac0ecea82fe71d01` |
| `xHnIi9GqOsM` | 5 Nov 11:30 | `6ae5e2a5ceb491e585f86c88` / `6ae5e2a6406ab8a018baadab` / `6ae5e2a7eaa24d6f9a755f79` |
| `LCZRHUyTiq0` | 6 Nov 11:30 | `6ae330c292ad728a4576d5ac` / `6ae330c3a0a200dca8ba714f` / `6ae330c4a0a200dca8ba71c6` |
| `OnJ8MFu0Mi0` | 7 Nov 11:30 | `6ae330c7bab0e956b96ce00f` / `6ae330c8ac0ecea82fe72466` / `6ae330c992ad728a4576d797` |

**Preserve all these dates.** The three apparent stale/old-video dates are deliberate back-post exceptions: [Chief's recorded Ben approval, HOS #180 comment 6495697066](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6495697066) explicitly names 4/6/7 Nov and the differing social source files. This is not a new replay request or a reason to delete/reschedule them. Registry/ledger source hashes agree; Herschel and Snow local hashes freshly match. Cathode local iCloud read currently fails `Resource deadlock avoided`; its existing R2 asset is accessible and Buffer reports processing complete, so this is a local future-rehost limitation, not evidence to replace a functioning queued asset. No full remote hash was computed.

All five queued R2 video URLs returned **206**, `bytes 0-1023/<size>`, from the Mini, with video MIME types (`range-checks.json`). Only 1 KB per file was read. The earlier cloud 403/1010 is not reproduced here. Buffer's asset metadata reports no processing/transcoding required for all scheduled videos; scheduled status is not a promise of successful eventual delivery.

Old HOS Curie Facebook receipt `6ade37890b5343d070e1ba0a`, video `AMSriTQ-lcQ`, is still `error`, due 28 Oct 11:30. Buffer says “An unknown error has occurred. Please retry the post again, and get in touch if this persists.” Instagram/TikTok were sent. **Do not retry it** under this recovery: late replay remains a separate decision and original approval scope must be checked.

## Established causes

1. **Daily wrapper locks itself out.** LaunchAgent is installed and loaded, calendar 07:05, three runs, last exit **75**. Installed plist equals repository plist. Logs on 1, 2 and 3 Nov each show the outer wrapper owning `youtube-buffer`, then its own command refusing that lock. An exact outer-wrapper `... -- npx tsx ... check --dry-run` reproduction returned **75**, without reaching API work. Direct `npx tsx ... check --dry-run` acquired the CLI's own real lock and succeeded for OWB and HOS separately. No lock bypass used. `ensureDeskLock` trusts inheritance only when owner pid equals `process.ppid`; the outer wrapper runs npx/tsx through intermediate processes, so the CLI fails that check and reacquires its own held lock. The code issue is supported by logs and reproduction, not inferred from a quiet ledger.
2. **Discovery is incomplete.** `data-api.ts:listRecentUploads` fetches a single page of 50; `listScheduledUploads` defaults to it. Live direct-id queries show Mars long `Js6EQJ8qDi8` scheduled 8 Nov 18:00Z and Mars night `iyvWYFP_ETA` scheduled 9 Nov 11:30Z, neither in the ledger/live queue. Playlist inspection over all 184 visible entries places the long at **60** and the night Short **absent from the entire returned playlist** (position 0 means not found). Querying registered ids is necessary; merely increasing the page size or paging once is insufficient for the absent Short. Titan is position 50. Daily dry-run therefore does not report the two Mars gaps at all.
3. **Source identity is unsafe for automatic Titan recovery.** Titan's registry/upload SHA is `afe0e80f044aca2887b9a9ef1d2aaf9fee9098285315fdc5d667eaca0019ca6c`; local v01 freshly hashes `3f2f51d4f8ffd1adfc0e9c0e91c25839198860e49c3085367ea876f341d606a2`. J1008 already documents the in-place 17 Oct rerender and no separate approval of that local hash. The ordinary dry-run still proposes it without checking SHA. A successful plan must not be treated as source approval.

Both profile ledgers' newest receipts remain 31 Oct 12:43/12:44Z; last established successful manual run is J1348 on 31 Oct (commit `0be81cb242`). Available daily log's last successful OWB output before the gap is 11 Oct; no successful daily HOS run is established by this log. 1–3 Nov stop before HOS starts. Current branch main, no tracked local edits and no unpushed commits at inspection. No unpublished social records explain the gaps. Existing untracked shared files were left alone. Disk ~7 GB; authorized NAS offload found nothing old enough to move.

## Exact proposed creates and holds

`prepared-plans.json` contains per-network action inputs, copy and metadata from the live YouTube record and existing registry. **All use dry-run placeholder URLs; never execute those inputs literally.** A recovery worker must re-read live state and hydrate only approved/hash-verified files via standard R2 route after elected-Chief scope approval. Re-read ledger plus remote queue immediately before every create; skip a matching existing video/network post, retain its id and do not duplicate a sent post. No blanket write-mode `check`: it includes cleanup and would accept the mismatched Titan source.

| Video | Unchanged YouTube go-public UTC | Networks / proposal | Source and readiness |
|---|---|---|---|
| `Js6EQJ8qDi8` (OWB:025 long) | 8 Nov 18:00 | IG/FB trailer Reels; Threads thumbnail; missing live posts | Registry/package trailer readable, SHA `7aa47737a87987b24ce09f322795bd9717d6488076a6c52dbcc9d42e0c9c16d4`; thumb readable, SHA `bb5e525b6fd9d72a753b179197cf4785a00a404bdfc6e0e23cdd5bca2f7a3e9d`. These are the source paths named by the original upload result. Missing full long master is not needed for these social posts. Three original upload receipts (`6ac94b3ec4de2d2b12057da8`, `6ac94b3fbba9419ccbdd4dd8`, `6ac94b3fbba9419ccbdd4e20`) now return Post not found and are absent from the complete listing. Classify as gone, not sent. Recreate only after Chief reviews this evidence and verifies no newer matching post. |
| `iyvWYFP_ETA` (OWB:025 Short) | 9 Nov 11:30 | IG/FB/Threads **held on exact source** | Expected upload SHA `48466c33946ed4367d0569a299062e5953ec9e05c7f745d1b4b7a4c9f24162e1`; local original absent, registry explicitly `knownNoFile` after J0432 overwrite. Original upload social creates all failed free-plan capacity. Explicit dry plan errors `--media-url: no URL given`. Restore a proven original or separately scope Studio Download/current-cut recovery; do not substitute a newer render or waive source checks. |
| `RLSJm59OSzI` (OWB standalone Titan) | 10 Nov 11:30 | IG/FB/Threads **held on source mismatch** | Local/expected SHAs above. Entered seven-day window only after today's 07:05 run; not a missed deadline on 3 Nov morning. Automatic scheduling on 4 Nov would pick wrong bytes unless guarded. Recover approved original or explicit separately reviewed source decision; existing gate/approval holds still apply. No new media approved here. |
| `PFj6172YU4Q` (HOS:005 tight band) | 8 Nov 11:30 | HOS IG/FB/TikTok, missing live posts | `hos_005_s02_the_tied_arm_v05.mp4`, SHA `c31fbb5c88f61b9bc2bbfae8b7a059b84b99575c5876066167ae22021ace70df` freshly matches registry. Parent `wwcjcFfC-5M` public; standard explicit dry plan has no errors and three creates. Ready for Chief's narrow hosting/create scope. |

No other current window missing-post create is established by these sources. OWB later uploads (11 Nov onward) and HOS current replacement ids `cLKDiYP55J8` (13 Nov), `Wvjd8g0CpzE` (15 Nov), `xzKoHg0E0_U` (16 Nov), `xgx2lYHhYZM` (17 Nov) are legitimately deferred outside the seven-day window. Preserve approved swaps; never revive old ids `-I_GHK-GcFs`, `x_3L_IdYgEc`, `-sa2t7dAtCk`, `4WUs0beKn0A`. Historical swap evidence is saved in `hos-approval-and-swaps.json`.

## Next decision and scoped implementation

One linked elected-Chief recovery job must:

1. Review this report and recheck election. Approve narrowly the two source-ready items (Mars long and HOS tight band), or give an evidence-specific hold. Authorize their R2 hosting and only missing network creates at the times above; no late/replay/deletion/reschedule/media change follows from J1870 itself.
2. Route a focused code PR: remove the daily npx self-lock conflict while preserving one real whole-command lock, refusal of a genuine other holder and cleanup on exit; discover registered scheduled ids through authenticated direct-id lookups as well as playlist; enforce source hash/explicit approved-social-source exceptions before hosting. Regression checks must exercise the exact wrapper→npx→tsx process chain and a registered scheduled id absent from the playlist. Do not weaken pid verification or use an env-only bypass. Do not run the daily write-mode job before the mismatched source has a fail-closed guard or an approved recovery.
3. Give the two blocked OWB Shorts specific source recovery owners/scopes. Keep YouTube dates, live files and existing approval gates unchanged. Cathode's local iCloud hydration is only needed if a future rehost is proposed; leave functioning queued asset alone.
4. Verify fresh scheduled ids/status/date/media metadata after any authorized creates, commit registry/receipts from a clean worktree, and report both organizations. No bulk cleanup, Curie retry, new service, credit spend or Ben sign-in request is needed by the proven faults.

This job ends at the audit/plan boundary. No recovery approval or film-stage PASS is asserted.
