# J1128 checkpoint — Codex worker, 28 Oct 2026

Work remains; no worker PASS, merge, spend or YouTube change.

## Measured findings

- Initial observed free space: 12,292 MiB (12.89 decimal GB), before the report worktree. Current checkpoint: 14.68 GB. J1112 reported 30.43 GB at 17:20Z. The job's 10.5 GB was an earlier reading, not this run's baseline.
- Recent competitor JSON in `_desk/j1106` and `_desk/J1107`: 4.087 GB in files over 10 MB modified since 17:20Z. A sampled 11.67 MB file held 11.20 MB of `automatic_captions`; those caption and format URL trees are unused by the research calculations. Total research detail caches are about 4.9 GB including earlier files.
- Swap: 9,216 MiB allocated, 7,675.81 MiB used. Four 1 GiB swap files have mtimes after 17:20Z. This is evidence of swap activity, not proof that all four were newly allocated or that a specific browser caused it. Five Chrome processes and about 50 renderers were observed. No browser was stopped and no swap file touched.
- No Time Machine or APFS Data snapshots. Hugging Face cache has not refilled; no Ollama model directory found. Ordinary Library caches were only about 199 MiB. Hidden studio Chrome profiles total about 3 GiB, with only about 1 GiB of rebuilding caches reclaimed below.
- Synology Drive daemon log is 952.5 MB, but J1112 already measured about 5 GiB for the whole app store, as now. Its last chunk has repeated errors; the historical growth of this file is not established. App databases, logs and sync settings retained.
- Main git stores: OWB about 1.2 GiB, HOS 915 MiB. Recent pack mtimes include J1112's gc, so they cannot be counted as new growth. No concurrent prune/gc run was attempted.
- The full historical ~20 GB drop is **not yet accounted for**. Do not report it as solved. Root/Containers sweeps stall on this Mac; bounded local scans supplied the usable measurements.

## Safe work completed

- `mini_repair.py --apply --json`: 11,806 -> 13,004 MiB free; removed three clean pushed temporary worktrees, kept dirty/unpushed ones and all edits. No reset or local-work deletion was needed.
- Cleared ten known rebuilding browser/GPU caches from J1112's own inventory: 1,026,096,191 bytes. Cookies, sign-ins, IndexedDB, chats and app databases retained. `caches.json` records paths and measurements.
- Patched the actual resumable collectors: `_desk/J1107/competitors/collect.py`, `_desk/j1106/competitors/collect.py`, `_desk/j1106/competitors/extra_study.py`. Only watch-detail JSON is compacted; channel tab entries remain intact. Public IDs, dates, views, durations, availability and thumbnail metadata remain. Copies in `collectors/` make the local changes reviewable; these collectors originated in other jobs and are not on main yet.
- Added `scripts/research_metadata.py` and a regression test. Unit test passes; AST-extracted compaction functions in all three actual collectors match the helper on saved research samples. No public data fetched or findings rewritten.

## Detached recovery: check, never duplicate

Two copies are active. Each checks a real mounted NAS, copies with rsync, compares full SHA-256 manifests, rechecks the source, and only then reclaims local bytes. No NAS file is deleted or overwritten.

1. tmux **J1128-recover**: `/Users/benjaminoats/_desk/logs/J1128-recover.log`, completion `/Users/benjaminoats/_desk/logs/J1128-recover.done`.
   Archives old `~/chief_tmp` (3.91 GB) and the two old Cursor studio artifact directories (1.83 GB combined). All three were untouched for over 48 h. Marker files retain the archive paths. Structured result: `~/_desk/logs/J1128/recovery.json`.
2. tmux **J1128-compact**: `/Users/benjaminoats/_desk/logs/J1128-compact.log`, completion `/Users/benjaminoats/_desk/logs/J1128-compact.done`.
   Preserves original JSON directories on NAS with checked manifests, then compacts local JSON in place. It does not remove thumbnails, studies, calculated rankings or IDs. Structured result: `~/_desk/logs/J1128/compact.json`. Expected recovery roughly 4–5 GB; actual result must be read after completion.

Launcher copies are in this pack. The running processes already loaded their scripts. Slow NAS transfers will exceed this worker's remaining bounded run; do not start replacements while `.done` is missing. NAS destinations are under `mac-mini-archive/mini-tmp-scratch/2026-10-28/`, with distinct `chief_tmp`, artifact and `J1128-...-details` folders.

## Next worker

1. Read both `.done` files and logs. Missing means running; leave alone. Nonzero means inspect the error and keep local data. Read the result JSONs once present.
2. Verify current free bytes and complete diagnosis/recovery to **30 decimal GB**. These selected archives plus compaction may not alone reach that target. No further broad deletion is authorised by this report.
3. Verify all three collector patches remain effective (the helper and sample checks pass now); ensure the other jobs' eventual collector commits use these patched copies.
4. Only after adequate recovery and the cause/fix are evidenced, reopen J1100 with measured free GB and a truthful note, preserving its step 1/3. It remains blocked in this checkpoint. Do not claim/render J1100 in this run.

Thread read to #6480506360.

## Resume 28 Oct 2026, Codex worker

- Resumed the existing PR #329 worktree and detached jobs; did not duplicate their copies. Current free space is 12.38 decimal GB. No target claim and J1100 remains blocked.
- Original `J1128-compact` exited 1 at the destination manifest comparison, before compaction. `J1128-recover` is still running on its third archive; its first two comparisons failed safely and retained local sources.
- Root cause of these comparison failures: NAS-generated AppleDouble `._` files. chief_tmp has 730 source files and 1,514 destination files; all 784 extras have `._` names. No source filename is missing. Sample metadata header is AppleDouble v2 (`0005160700020000`). This filename survey alone is not checksum approval.
- Added `verify_archive.py`: all original size/hash pairs must match, and extra files are accepted only if they have AppleDouble v2 headers and a corresponding source file/directory. Missing files, changed payloads, unrelated extras and invalid metadata fail closed. Regression test passes. Existing research-metadata regression also passes.
- Started **tmux J1128-resume**, log `~/_desk/logs/J1128-resume.log`, completion `~/_desk/logs/J1128-resume.done`, structured result `~/_desk/logs/J1128/resumed.json`. It reuses the existing first two archives, checks all SHA-256s and source stability, then reclaims local old scratch. It reuses the J1107 original JSON archive and verifies/compacts the remaining research directories. It waits for the original recover `.done` before touching that worker's final archive. No NAS deletions or overwrites of media. Launcher is `resume_recovery.py` in this pack.
- Live swap has grown from the prior checkpoint's 9 GiB allocation to **10 GiB allocated / 9,133.81 MiB used**. No swap files touched, browser stopped, or attribution to a particular process claimed. Historical 20 GB growth is still only partly explained by research JSON plus swap activity.

### Next continuation

Check `J1128-resume.done` and `J1128-recover.done` plus their logs and structured results; missing means leave running, never duplicate. Verify free space after recovery; target remains **30 decimal GB**. If incomplete, inspect the exact failure and retain local data. The NAS helper workaround is job-local, not a change to shared core. Ensure collector patches are preserved by J1106/J1107. Reopen J1100 only once the required recovery and cause/fix evidence are complete. No PASS, merge, spend, upload or schedule change.

Thread read to #6480842882.

## Continuation 21:43Z, Codex worker

- Resumed the existing worktree/PR 329 and preserved the four-step plan at step 1. No second copy started.
- `J1128-resume` has now completed checksum-verified moves of chief_tmp and OWB worker artifacts, and verified archive plus local compaction of all three research detail directories (1,106 + 287 + 711 files). Structured evidence remains in `~/_desk/logs/J1128/resumed.json`. J1107 now totals 76 MiB, j1106 586 MiB including its 489 MiB review worktree.
- Live free space: 19,484,168,192 bytes (19.48 decimal GB), versus this continuation's initial ~17.6 GB. Still below 20 GB render floor and 30 GB target; J1100 stays blocked. Free bytes fluctuate with live work.
- Read-only process check confirms original rsync PID 1804 is still copying HOS worker artifacts to `artifacts__2` on NAS. `J1128-recover.done` and `J1128-resume.done` are both absent. Resume waits for original recovery, as designed. Leave both tmux sessions alone.
- Live swap now 11 GiB allocated, 10,034.50 MiB used (previous checkpoint 10 GiB allocated). No swap files touched, no browser stopped, and no unsupported attribution. The full historical drop remains partly unaccounted for. Time Machine still has no local snapshots. Ordinary caches remain about 199 MiB; standard Chrome profile about 1.1 GiB.
- Archive verifier and research metadata regression tests both pass. Existing collector compaction fix remains the evidenced recurrence mitigation; no new code change was necessary this continuation.
- Required `nas_offload.py --apply` completed with no eligible old /private/tmp scratch; no NAS data deleted. No media masters or UAT files touched. GBP0.

Next: check both completion files/logs and the final archive verification; continue diagnosis and safe recovery to 30 GB, then reopen J1100 only with measured headroom and truthful cause/fix evidence. Do not duplicate the active copies.
