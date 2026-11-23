# J2037 — Specialist Package Verification & Private-UAT Staging Prep (HOS 009 Long Master v03)

- **Job:** `J2037` (*HOS 009: Review HOS009 finished pack and deliver Ben watch card*, ref `J2026`, `HOS:009`)
- **Agent & Role:** `gemini` (specialist worker on the Mac mini; **not** elected Chief; rerouted by Acting Chief Codex in OWB `#954` comment `7114947415` for specialist package review while keeping protected final calls with the elected Chief)
- **Date:** 23 Nov 2026
- **Recommended Specialist Verdict:** **KEEP (private UAT handoff ready)** — **PARKED FOR ELECTED NON-PRODUCER CHIEF** (no self-PASS, no self-merge, no worker `awaits_ben`)
- **Spend:** £0.00 cash · 0 Flow credits · 0 ElevenLabs credits · 0 YouTube / Studio / Buffer / schedule / privacy changes

---

## 1. Authority & Non-Producer Independence Disclosure

1. **Worker authority boundary:** Live `chief_relay.py status` confirms `gemini` is a specialist worker, not the elected Chief (`Codex` elected at claim `21:49Z`; `Claude` returned `UP` after `21:50Z`). Final PASS, PR merges, and arming Ben's `jobs.py awaits` watch card are protected Chief decisions.
2. **Producer independence:** `gemini` built `J3314` (`hos009_long_master_v03.mp4`, HOS PR `#719`) and authored `J2036` (HOS PR `#731`). Consistent with the `J3311` non-producer Shorts review precedent (`23 Nov 2026`), `gemini` does **not** self-PASS, self-merge PR `#731`, or arm `jobs.py awaits`. This run completes every tool-provable check, resolves PR `#731`'s merge conflict, stages both the exact-hash v03 master and a `<120 MiB` phone watch proxy to NAS + HOS UAT, and parks the protected final ruling for the elected non-producer Chief.

---

## 2. Exact-Hash, Probe & Full-Decode Verification (23 Nov 2026)

### Master & Watch Proxy (3-Way SHA-256 Parity Verified Live)

| Artifact | Paths Verified | Bytes | SHA-256 | Probe / Full Decode |
|---|---|---:|---|---|
| **v03 long master** | NAS `09_Assembly/j2035_v03/hos009_long_master_v03.mp4`<br>Mini scratch `J3314-assembly/hos009_long_master_v03.mp4`<br>`HOS UAT/009_The-Falling-Moon-Gravity/hos009_long_master_v03.mp4` | `898,035,226` | `744f32b7f2f95e75fabf039a345aee6c7c01ab6f304a932ebe7172bd3b3ede55` | `519.000000 s` (`8:39.0`), `1920x1080` h264 30 fps (`15568` frames), AAC 48 kHz stereo (`24330` frames), `ffmpeg -v error -f null -` **exit 0** |
| **v03 PHONE watch proxy** (`< 120 MiB` `WATCH_AUTO_MAX`) | Mini scratch `J3314-assembly/hos009_long_master_v03_PHONE.mp4`<br>NAS `09_Assembly/j2035_v03/hos009_long_master_v03_PHONE.mp4`<br>`HOS UAT/009_The-Falling-Moon-Gravity/hos009_long_master_v03_PHONE.mp4` | `76,781,219` (`73.2 MiB`) | `b1135b3d36961afd283439e294d7f978ff1f107507d1b60d0d842c91107c5871` | `519.000000 s`, `1280x720` h264 30 fps + AAC 48 kHz stereo (`-movflags +faststart`, `1,183.5 kb/s`), full decode **exit 0** |

> **Why the PHONE proxy was built:** `scripts/kanban_snapshot.py` enforces `WATCH_AUTO_MAX = 120 MiB` (`125,829,120` bytes) for auto-uploading UAT cuts to Cloudflare R2 `/api/watch` Play links. The full 1080p master is `856 MiB` (`> 120 MiB`), so matching HOS 008's precedent (`hos_008_master_v05_PHONE.mp4`), `hos009_long_master_v03_PHONE.mp4` (`73.2 MiB`) was transcoded directly from verified `744f32b7...` at £0 and staged beside the full master. No R2 upload or `watch_uploads.json` edit was performed prior to Chief PASS.

### Untouched Prior Masters, Stems & Locked Inputs (Recomputed Live)

| Asset | Verified SHA-256 | Status |
|---|---|---|
| Prior master `v02` (NAS) | `9d8731cb49641776027bcbd75a6f4ae5519fc3907c28cb7f422883ebde73ef10` | Untouched |
| Prior master `v01` (NAS) | `802b5c7eb0dd64a77b938e5f26c2f63104c3b851979dabe61e39e70eaf33a833` | Untouched |
| `stems/vo_stem.wav` (NAS) | `f00a4af2bf3971215f0ef88288519fee9505fce35f47fc2cc8ed6ad1fd90ab94` | Present |
| `stems/bed_stem.wav` (NAS) | `40cd660684d6e5593fb504f4e813431fb80bf383d43af77e3c63a1ad60d0a20e` | Present |
| `stems/sfx_stem.wav` (NAS) | `cdb0172e2b46eb9a2be362e05a382aecf9d352aa1fc7d317417597900c6db787` | Present |
| `02_Voiceover/VO_TAKES_KEEP.json` + 5/5 locked VO MP3s (HOS + NAS) | `530743c507af8d5f9049179d4e9d380b5c1b8aca4f180ada133d0b673f5925e0` · Parts 01–05: `81b6c45f…`, `36855907…`, `53235ab0…`, `2d03f372…`, `10ebaf45…` | 5/5 exact match HOS & NAS |
| `05_Music/hos_009_score_v04_synth.wav` (NAS, J3241 accepted) | `151ba46acdf7d4395b34e105530bd077c26f6eb92832f9a1f00e1551ca88f58d` | Exact match |
| `J2631` `code_graphic_009_p4_05_minute_second.mp4` (HOS + NAS) | `e35f9a9879c8e590ec66853b85307999f39bfe30c67b9bed193ca224cab42da3` | Exact match (used in `SOURCE_MAP.json`) |
| `J2632 r4` `code_graphics_v01/J2632_r4/code_graphic_009_p3_01_really_falling_c1.mp4` (NAS) | `23c832b09e70f78d8eeece657dac11d6148e2a5f5c701f2ad88b868845b5f3b3` | Exact match (used in `SOURCE_MAP.json`; note older r1 file at parent path is `73e77846…` and is NOT used) |
| `J3262` Thumb A (`IT / MISSES`, HOS + NAS) | `cd44f05657ddfea2d9af1ad19f31c008479c43cbfa533a4e4800d90ed1186689` | Exact match HOS & NAS |
| `J3262` Thumb B (`ONE / APPLE`, HOS + NAS) | `3d1164330249e7793c96317b051d008271aaf4b90175bdddc86c392c979f1709` | Exact match HOS & NAS |

---

## 3. Delivered Gate Logs, Locks & Contract Verification

### Delivered v03 Gate Logs on NAS (`09_Assembly/j2035_v03/gates/`)

Verified on disk (not claiming a fresh re-run of `picture_qa`/`polish_gate`/`music_gate`/`sfx_kit` in this turn; J2036 independently re-ran all four on 22 Nov 2026):
- `picture_qa`: **PASS** — `92 cuts · 0 fail · 5 for Claude to look at full size` (`1:25` chapter card, `3:04` `01_really_falling` J2632 r4, `4:21` chapter card, `4:54` `02_spray_paint_c2`, `5:26` `05_minute_second` J2631).
- `polish_gate`: **PASS** — `polish gate PASS: 0 of 92 rows failed, 5 to look at`.
- `music_gate`: **PASS** — `hos_009_score_v04_synth.wav, 535.3 s, about 52.2 BPM, brief Pace: 60-68 BPM` (`fail: []`, `warn: []`, `waived: []`, `matches: []`, `waiver: null`).
- `sfx_kit level`: **PASS** — `SFX level PASS: VO -20.8 LUFS, SFX -41.4 LUFS, 14 hits`.
- `reviewed_ok.json`: unchanged, strictly **2** Grok rulings only (not widened):
  1. Grok `6792271903`: `P05:11_table_three_again` callback reuse of `P01:03_table_three` at `0.30–7.00 s` (inside J1237 `0–7 s` lock).
  2. Grok `7046684862` (20 Nov 2026): approved wooden-arch split panel on `P04:05_minute_second` only.

### J1237 / J2026 / E2 / Teach-on-Screen Verification (`SOURCE_MAP.json` & `FACT_NOTES_v01.md`)

- **J1237 / J2026 locks honored exactly:**
  - `P01:03_table_three`: `src_in=0.0`, `src_out=3.9925` (inside `0.000–7.000 s` lock).
  - `P04:07_put_aside`: `src_in=0.0`, `src_out=3.76` (exact lock, `<= 7.042 s`).
  - `P04:10_write_it_down_c1`: `src_in=1.083`, `src_out=6.423` (exact lock, `>= 1.083 s`).
  - `P05:11_table_three_again`: `src_in=0.3`, `src_out=7.0` (exact Grok ruling `6792271903`).
- **E2 First 30 s (`HOS-2026-11-E2`):**
  - First 8 cuts (`0.000–31.940 s`): 8 distinct moving plates (`01_moon_falling`, `02_apple_and_moon`, `03_table_three`, `03_table_three_c1`, `03_table_three_c2`, `09_stone_and_moon`, `07_night_field`, `12_still_up_there`), each `3.9925 s` (`< 4.5 s`).
  - `0:05–0:15` PROOF window verified (`verify_006s.jpg` falling Flower of Kent apple + Moon; `verify_010s.jpg` apple, brass cannon, parchment sum).
  - `0:25–0:40` EARLY DATA+SCALE verified (`THOUSANDS OF YEARS` cream-on-brown teach card `26.15–29.75 s`, `3.60 s <= 4.0 s`).
- **33 Teach & Label Cards (`card_verification` PASS):** `17 label`, `8 when`, `4 fact`, `2 who`, `1 data`, `1 timeline`; `0` overlaps, `0` chapter bleeds, `0` cross-shot drifts, `TWO SETS OF RULES` once only.
- **Script & `FACT_NOTES_v01.md`:** `review:script` **91.3 / 100 PASS**, `gate:episode` **PASS**, 7/7 hard-checks PASS (`FACT_NOTES_v01.md` lines 3 & 77 record Claude's 4 Oct 2026 confirmation; reconciled truthfully without inventing any new sign-off).

---

## 4. Direct Visual & Spot-Check Audio/Video Inspection (Honest Scope)

This session recorded demonstrated `image_input,audio_input,moving_video_input` via `chief_relay.py capabilities` after directly inspecting media with `read_file`:
- **Thumbnails A & B (`J3262`, Acting Chief PASS 21 Nov 2026):** Inspected `hos_009_thumb_A_it_misses_v01.jpg` (`IT / MISSES`), `hos_009_thumb_B_one_apple_v01.jpg` (`ONE / APPLE`), `hos_009_thumbs_v01_family.jpg`, and both 168×94 `_preview.jpg` sheets. HOOK, BAND, PHONE (168×94), family consistency with 001–004, and Explorer on-model all read cleanly; neither repeats the title.
- **1080p v03 stills inspected:** `verify_006s`, `verify_010s`, `verify_028s`, `verify_097s` (`ISAAC NEWTON / 1642–1727 · CAMBRIDGE STUDENT`), `verify_103s` (`25 DECEMBER 1642`), `verify_141s` (`NEVER HIT HIS HEAD`), `verify_299s` (`SIXTY EARTHS`), `verify_306s` (`SIXTY TIMES SIXTY`), `verify_322s` (`1 SECOND`), `verify_371s` (`1642 · 1665–1667 · 1684 · 1687 · 1758 / TWENTY YEARS`), `verify_433s` (`FALLING, TOGETHER`). All cards are crisp Didot italic on dark-sepia plaques or parchment ribbons, legible at phone scale, zero stacked captions.
- **Two short v03 mp4 spot-checks (`open_0_10s.mp4`, `early_data_25_33s.mp4`) — NOT a full 8:39 watch:**
  - Heard clear Ben Orbit Narrator British VO, warm gentle chamber bed underneath, and subtle pen-tap ink tick when `THOUSANDS OF YEARS` animated in (`26.15–29.75 s`).
  - **Transparent visual observation for Chief & Ben:** On frame `0:04.0` of `open_0_10s.mp4` (first frame of cut 2, Chief-KEEP Tranche 1 clip `02_apple_and_moon`), the falling apple shows a brief 1-frame Veo morph/split right at cut-in before becoming a clean whole Flower of Kent apple across `0:05–0:07`. Per `studio/RULES.md` line 90 (*"Plates already marked KEEP are used in the edit; this experiment does not authorise a remint"*), no remint is authorized; flagging transparently for the Chief and Ben's watch.
- **Full finished-cut watch/listen:** **NOT claimed.** Per Ben's 4 Nov 2026 standing order, full moving-video/audio watch and listen of the 8:39 cut remains Ben's final UAT watch.

---

## 5. HOS PRs & Package Contract Status

1. **HOS PR `#731` (`gemini/J2036-009-v03-qa`):** Was `CONFLICTING` with HOS `main` due to `J2171` (PR `#718`, merged `61fe58f4`) and `J3311` (PR `#736`, merged `2259b027`) updating `status.json` and `production-status.md`. Resolved cleanly in an isolated worktree by merging `origin/main`, preserving `main`'s `J2171`/`J3311` Shorts UAT records verbatim while keeping `J2036`'s v03 QA pack, honest making-of line (`moon_long_description_v01.txt`), exact v03 chapters (`0:00`, `1:24`, `2:56`, `4:20`, `6:33`), and all 8 Sources (`J1275` HOS 010 untouched).
   - Pushed head: **`e1f4f687ce7a1c0b720129242b6db2fac738101a`**
   - Local `check_all.sh 02_Video-Projects/009_The-Falling-Moon-Gravity`: **`ALL CHECKS PASS`** (including `package-lint: PASS`, `contract tests: PASS`, `review:script: 91.3 PASS`, `gate:episode: PASS`, `status board in sync: PASS`).
   - GitHub state: **`OPEN`**, **`MERGEABLE`**, **7/7 CI checks `SUCCESS`** (`no-desk-close`, `contract`, `no-media`, `status-board`, `check`, `tests`, `atempo`; `reopen-desk` intentionally `SKIPPED`). **Left unmerged for elected Chief.**
2. **HOS PR `#719` (`gemini/J3314-009-v03-status`, `75b4212c`):** `CONFLICTING` and fully superseded by PR `#731`. **Left open for elected Chief to close as superseded.**
3. **Shorts & thumbnails visibility (separate requirements preserved):**
   - `J0862` Shorts VO: PASS (`PR #423`).
   - `J2171` Shorts A & B assembly (`PR #718` merged `61fe58f4`) + `J3311` non-producer Chief review (`PR #736` merged `2259b027`): PASS for private UAT only; ordered `awaits_ben` cards `J3311.1` (Short A v01 `43dbeb3a`) and `J3311.2` (Short B v01 `e6e5ae3f`) are live and due `2026-11-24T18:00Z`. Ben's watch/listen pending; neither Short may air before the 009 long reads Public.
   - `J3262` long thumbnails A (`IT / MISSES`) & B (`ONE / APPLE`): Acting Chief PASS (21 Nov 2026), wired in `PACKAGE_MANIFEST.json`, awaiting Ben's final package approval alongside the long cut.
   - `ben_ok` and `scheduled` remain `todo`. Historical `26 Nov 18:00` long air date is internal planning only, not a verified upload or release promise. No YouTube, Studio, Buffer, schedule, or privacy changes authorized.

---

## 6. Exact Next Actions Parked for Elected Non-Producer Chief

1. Recheck live `chief_relay.py status` (confirm elected non-producer Chief: `claude` or `codex`).
2. Independently verify `hos009_long_master_v03.mp4` (`744f32b7f2f95e75fabf039a345aee6c7c01ab6f304a932ebe7172bd3b3ede55`) and `hos009_long_master_v03_PHONE.mp4` (`b1135b3d36961afd283439e294d7f978ff1f107507d1b60d0d842c91107c5871`) on NAS + `HOS UAT/009_The-Falling-Moon-Gravity/`, review the 0:04 apple-drop note and delivered gate logs/stills, and issue the non-producer Chief PASS for private UAT only.
3. Merge clean HOS PR `#731` at exact reviewed head `e1f4f687ce7a1c0b720129242b6db2fac738101a` (7/7 CI green) and close superseded HOS PR `#719`.
4. Arm Ben's UAT Ready-for-OK card on `HOS:009` with a verified working HTTP 302 Play link (`HOS UAT/009_The-Falling-Moon-Gravity/hos009_long_master_v03_PHONE.mp4`, `<120 MiB` for R2 auto-upload, keeping full 1080p master `744f32b7...` beside it) and a truthful deadline (matching `J3311`'s `2026-11-24 18:00` London or Chief-chosen truthful deadline):
   ```bash
   python3 scripts/jobs.py awaits J2037 --agent <chief-id> \
     --what "Watch HOS 009 Gravity long master v03 (sha256 744f32b7; 720p watch proxy b1135b3d) + approve thumbs A/B" \
     --file "HOS UAT/009_The-Falling-Moon-Gravity/hos009_long_master_v03_PHONE.mp4" \
     --version v03 --card HOS:009 --type long \
     --due "2026-11-24 18:00" \
     --if-not "Keep private and unscheduled until Ben watches and approves (no upload or schedule without OK)" \
     --git
   ```
5. Verify the published signed Play link returns HTTP `302` (`board_publish.py` / `board_check.py`), leave `J2037` / `ben_ok` parked for Ben's actual finished-cut watch & listen, and authorize publishing only separately after Ben's approval.
