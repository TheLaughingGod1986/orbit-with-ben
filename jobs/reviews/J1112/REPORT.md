# J1112 — Mini disk cleanup, 28 October 2026

Worker: codex. GBP0. No media or personal app data deleted. No NAS files changed.

## Result

Free space rose from 14,123 MiB (14.81 GB) to **30,433,521,664 bytes (30.43 GB / 28.34 GiB)** before the temporary report worktree. The brief says 30 GB; this is decimal GB, not 30 GiB. J1100’s 20 GB prerequisite is cleared. Chief/relay owns reopening that blocked job; this worker did not start another job.

## Actions and evidence

- `mini_repair.py --apply`: 14,123 → 21,853 MiB free. Removed 17 clean pushed temporary OWB worktrees; retained dirty and unpushed worktrees, including J1100. Package cache cleanup ran. Full output: `repair.json` (text output despite extension).
- Time Machine: `tmutil listlocalsnapshots /` returned no snapshots; `tmutil thinlocalsnapshots / 999999999999 4` completed with none listed.
- Cleared 48 recognised Chrome/Cursor/updater cache directories, measured at 1,499,608 KiB, then studio Chrome profile caches measured at 3,239,252 KiB. Path/size inventories: `caches.json`, `profile-caches.json`. Cookies, sign-ins, IndexedDB, chats and User/globalStorage retained.
- Cleared the downloadable Hugging Face cache (2,955,857,920 bytes reclaimed). No voice checker was running. **Next local model use may download models again**, with no API spend. See `model-cache.json`.
- `git gc --prune=now` ran in both repos. HOS `git lfs prune`: 0 objects, 1 retained. OWB retry after recovery: 0 objects, 1 retained.
- OWB compaction raced the queue progress commit, leaving missing local commit `94eb85564f09d2077e1048b88cf10e549e5847e1`. Restored its preserved queue blob and recreated the commit with the original index tree, parent, author, timestamp and message: **the identical hash**. No reset, branch rewrite or working-file loss. Avoid concurrent `--prune=now` and queue writes in future. A direct main push was rejected by automatic review; evidence showed only queue progress was pending, and the explicitly required `jobs.py progress --git` was subsequently approved and succeeded.

## Survey and exclusions

Size-only surveys covered home top-level, Library Caches/Application Support/Containers, Downloads, Movies, private tmp, desk scratch/renders/worktrees and both repo git stores (OWB initially 1.0G, HOS 954M). Broad home/Containers scans timed out; bounded scans and targeted surveys supplied the usable sizes. Full local diagnostic logs remain in `~/_desk/logs/J1112/`.

Largest retained app data: Cursor globalStorage ~5.2 GiB and chats ~3.7 GiB; SynologyDrive ~5 GiB. Retained all personal folders, app databases, installed extensions, environments, studio render packs and protected cut versions. Downloads ~879 MiB; Movies ~48 KiB. Desk renders ~2.85 GiB were J1032 variants used by pending work, so retained.

NAS offload dry run at 30 GiB target found no eligible >=200 MiB scratch directories older than 48 hours. No offload was needed to reach the brief’s decimal 30 GB target. No NAS deletion or media spend.

## Next

Chief/relay: resume J1100 after reading the current free-space measurement; retain the 20 GB render guard. Cleanup complete; report submitted for Chief review, with no worker PASS or merge.
