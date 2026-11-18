# WW2:001 picture preparation — J2993

18 Nov 2026 · Codex covering · **Work in progress, not a finished cut or QA PASS.** £0 spent.

## Delivered

- `harvest_archives.py`: resumable exact-ID archive search/download, with catalogue links, creator, caption, dimensions, public-domain metadata and SHA-256. Candidates require caption/licence review; search results are never KEEP. Rate limits are respected and checkpoint writes are atomic.
- `align_shots.py` and `shot_anchors_v01.json`: 50 draft shot anchors aligned to the existing Scribe word times through 1,656.7 seconds. All are unique, ordered and contiguous after the first word at 0.16 s. Four fuzzy matches below 0.85 need attention: S01, S14, S19, S24 (dates, spelling and spoken numbers). These are not watched/heard checks.
- `draw_channel_map.py`: own 1920×1080 G11 Channel map, with a 12-second animated connection build. Labels and endpoint visibility inspected as stills; encoded H.264 file fully decodes. Connections are explicitly schematic, not historical convoy tracks. Natural Earth geometry and public-domain terms recorded in `map_geography_provenance_v01.json`.
- `build_thumbnail.py`: two 1280×720 drafts from IWM BU 1024, normal/bright black-and-white treatment: A archive only, B **FLOATING PORT**. Original, crop, grade and hash in `thumbnail_recipe_v01.json`. Original and 168-pixel previews visually inspected; no invented “12 days” claim. Final selection/licence review remains.
- Map v02, both thumbnails and comparison/phone previews copied to the existing studio-live WW2 film folder; all **7 files SHA-256 matched**, recorded in `prep_media_sha256_v01.json`. No media committed to git.

## Inputs and issues

- Script/shot-list source is **open OWB PR #996**, branch `macbook/J2991`; VO source is **open OWB PR #998**, branch `gemini/J2992-ww2-001-vo`. They have not been merged by this job. Script/shot list extracted read-only under `/tmp/J2993-inputs/`; the authoritative narration already exists on studio-live.
- NAS film: `/Volumes/data/studio-live/ww2/02_Video-Projects/001_Mulberry-Harbours-Floating-Ports-D-Day/`. Narration is `02_Voiceover/mulberry_harbours_vo_v01.wav` and its Scribe file is `02_Voiceover/stt/mulberry_harbours_vo_v01/stt_raw.json`.
- Working cache: `/Users/benjaminoats/_desk/ww2/J2993/`. At this checkpoint 15 IDs had been attempted and 8 candidate files downloaded; see `archive_candidates_checkpoint_v01.json`. The live manifest in the cache supersedes this snapshot.
- Some IWM mirrors are only 800 pixels wide. Obtain larger originals or use crops/insets at appropriate size; do not assume they are good full-screen sources.
- BU 1024 mirror identifies Sgt Harrison / No 5 Army Film & Photographic Unit and the official War Office collection, with `PD-scan (PD-UKGov)` metadata. Primary IWM catalogue `https://www.iwm.org.uk/collections/item/object/205021912` returned **403** through the browser tool, so primary verification is recorded as pending, not falsely passed.
- Some planned shots have a collection rather than a unique image ID (e.g. S06). S23 proposes a Tate painting and S04 a Canadian item: neither is automatically cleared under the current channel rule's US/UK official-photo restriction. Substitute eligible official photographs or obtain a specific documented Chief ruling; the upstream blanket “verified” label is insufficient.
- Estimated shot-list times are not the edit timeline. Use the draft audio anchors and inspect joins against Scribe before assembly.

## Resume

The job is longer than one unattended run. A single downloader continues in **tmux `J2993-archive`** using this worktree. Do not start another while it runs.

- Worktree: `/tmp/J2993-wt`, branch `codex/J2993-picture-prep`.
- Log: `/Users/benjaminoats/_desk/logs/J2993-archive.log`.
- Completion: `/Users/benjaminoats/_desk/logs/J2993-archive.done` (missing = still running).
- Launcher: `/Users/benjaminoats/_desk/ww2/J2993/continue_archive_harvest.sh`.
- A zero downloader exit means the pass ended; inspect every manifest status. It does **not** mean every record resolved or any candidate is approved. Errors are retryable; unresolved IDs and caption mismatches need research.

Next: finish/archive-caption and rights checks; replace unsuitable/underspecified shots; inspect all 50 anchors; draw remaining graphics; assemble to narration with a new WW2 score under the existing plan; prepare chapters, credits and upload package; run applicable technical gates and still review; then Chief submits the finished cut for Ben's watch. No upload, channel creation, paid service, or public state change is authorised by this handoff. No full watch/listen or completed film QA is claimed.
