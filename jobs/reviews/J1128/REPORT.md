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
