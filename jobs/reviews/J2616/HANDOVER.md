# J2616 handover: approved_deliver.py, 35 channel lines to 0

MacBook run of 11 Nov 2026. The reading and the design are done; no code is changed yet. The run stopped
because the job turned out to need a change in both repos (see "Why two repos") and would not fit in 25 minutes
with the tests. Start from here; do not re-read the script to find the lines.

## The 35 counted lines (main at 708041eaf)

| Lines | What |
|---|---|
| 36, 40 | `CADENCE` keyed by the two labels |
| 201, 243, 245, 374 | `or "OWB"` and `CADENCE["OWB"]` fallbacks |
| 216-219, 222-225 | `taken_cadence_days`: one UPLOADS.json branch per channel |
| 393 | the Buffer body's TikTok note for one channel |
| 407, 408 | `film` / `stage` only for the home channel |
| 409, 435 | `repo` slug by name |
| 472 | `def load_owb_films` |
| 493, 495, 498, 500, 501, 503, 505, 508, 511, 512, 515 | `load_hos_pipeline` and its locals, and the import of `attach_hos_uploads` |
| 539, 540, 544, 545 | `load_delivery_videos`: locals and the `hos=` / `owb=` keywords |

## Design (each keeps today's behaviour for the two channels)

1. `import channels` at the top (the two lazy imports go).
2. **Cadence moves to the channel file.** New field in `studio/channel.json`:
   `"cadence": {"long": [[6,18,0],[2,18,0]], "short": [[0,11,30],[2,11,30],[4,11,30],[5,11,30]]}` (Orbit) and
   `{"long": [[3,18,0]], "short": [[5,11,30],[4,11,30],[6,11,30],[1,11,30]]}` (History of Science). Order matters:
   keep it exactly as in the script. New loader function `channels.cadence(slug)` returning
   `{"long": [(wd,h,m),...], "short": [...]}`, reading the channel's file and then the cached copy, the way
   `planned_shorts` does, `{}` when neither names one. In the script: an unknown channel, or one with no cadence,
   uses the default channel's (`channels.default()`), and a kind with no slots uses the default channel's long
   slots: that is what `CADENCE.get(ch, CADENCE["OWB"]).get(kind) or CADENCE["OWB"]["long"]` does today.
3. `or "OWB"` becomes `channels.label(channels.default())` (not `channels.home()`: that would add to the home
   ratchet, where this script has no entry).
4. `taken_cadence_days`: one branch for any channel:
   `c = channels.get(ch); base = root if c.get("home") else channels.repo_path(c["slug"])`, then
   `base / "00_Brand" / "Channel-Setup" / "social" / "UPLOADS.json"`, `_uploads_publish_days(..., channel=ch, ...)`,
   all inside `try/except Exception: pass` (an unknown label reads no file, as today). `test_uploads_json_blocks_...`
   passes `root=` for the home channel, so the home branch must keep using `root`.
5. Line 393: new field `"social": {"tiktok": "buffer"}` in the History of Science file only, loader function
   `channels.tiktok_by_buffer(slug)` (file, then cached copy), and the text becomes
   `f"; {channel} TikTok stays Buffer-only"`. Same string for HOS, nothing for Orbit.
6. Lines 407-409, 435: `film` and `stage` are set when `channel == channels.label(channels.default())` (the queue
   can only claim a stage on the default channel's board); `repo` is `channels.get(channel)["slug"]`, else
   `channels.default()` on KeyError; `repo=a.get("repo") or channels.default()`.
7. Lines 472-545: `vt.build_videos` already takes `documents={slug: doc}` (video_tracker.py line 1198). Rename
   `load_owb_films(root)` to `load_status_films(root)` and `load_hos_pipeline(root)` to `load_pipeline(slug)`; in
   `load_delivery_videos` build `documents` by `channels.pipeline(slug)["kind"]`: `film_status` for the home
   channel -> `load_status_films(root)`, `pipeline_json` -> `load_pipeline(slug)`. Give no document to a channel
   of any other shape: `build_videos` then reads it through `channel_films`. No test or other script calls the two
   old names (checked: only `board_publish.py` runs the script, by path, and `test_listing_deliver.py` uses
   `load_delivery_videos`, `plan_actions`, `taken_cadence_days`, `next_cadence_slot`, `same_cut_identity`,
   `passed_candidates`, `LONDON`, `lp`).
8. Line 511, the import of `kanban_snapshot.attach_hos_uploads`: the name itself is counted. Rename the function
   in `kanban_snapshot.py` to `attach_pipeline_uploads` (its `def` and call lines stay counted there for their
   other names, so that script's ceiling does not move) and update its callers
   (`grep -rn attach_hos_uploads scripts`). Check `studio-core/CORE_FILES.json` first: if `kanban_snapshot.py` is
   core-locked, it needs `core_sync.py lock` and a push to the other repo.

## Why two repos

`test_channels.OwnRepos.test_the_cached_copy_matches_the_channel_repo_when_it_is_here` fails wherever the History
of Science checkout is present (the Mini, the MacBook) unless `channels/hos/channel.json` is byte-identical to that
repo's `studio/channel.json`. So the two new fields (`cadence`, `social.tiktok`) need a small pull request in
history-of-science adding them to its `studio/channel.json`, and the same text in `channels/hos/channel.json` here.
Until that one merges, the loader reads the cached copy for the missing field (the `planned_shorts` pattern), so
the live studio's slots do not change in between. Say this in both pull requests.

## Tests to add

- `scripts/test_channels.py`: `cadence()` and `tiktok_by_buffer()` for the two channels, for a made-up `sky`
  channel with and without the fields (`TrackerAsksTheLoader.sky(...)` is the helper), and the cached-copy fallback
  (copy `test_a_checkout_behind_main_takes_the_setting_from_the_cached_copy`).
- `scripts/test_listing_deliver.py`: a `sky` channel with its own `cadence` gets its own slot from
  `next_cadence_slot("SKY", ...)`, a `create` action for a SKY card carries `repo: "sky"`, no `film`/`stage`, and
  no TikTok note; and a test that pins today's slots for the two real channels to the literal weekday/time lists,
  so the move of the table out of the script is proved to change nothing.

## Then

`scripts/channel_ratchet.json`: remove the `approved_deliver.py` line and take 35 off `total` (edit by hand on the
MacBook: the ratchet script itself cannot be run there, `python3 -m unittest discover -s scripts -p
"test_channel_ratchet.py"` can). Run `test_listing_deliver.py`, `test_channels.py`, `test_channel_ratchet.py`,
the board and tracker tests, then the four checks in the brief. Dry run only: `python3 scripts/approved_deliver.py`
with no flags; compare its action list before and after the change.
