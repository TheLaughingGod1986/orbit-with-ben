# J3599 — Independent Review of `WW2:001` Mulberry Harbour Test Short (`v01`, `J3542`)

- **Reviewer:** `macbook-2` (review lane, MacBook worker; elected Chief is `codex` per fresh `chief_relay.py status`)
- **Reviewed at:** `2026-11-24T18:04-18:12Z`
- **Target cut:** `ww2/02_Video-Projects/001_Mulberry-Harbours-Floating-Ports-D-Day/Shorts/Mulberry_Test_v01/mulberry_short_v01.mp4` on the NAS
- **Exact master SHA-256:** `30b6a3a3de762dcbb5d0ea941c275058c4bd284352ad0450312d2e3b9f85d11b` (`20,087,314` bytes)
- **Parent job:** `J3542` (`WW2:001` edit; Ben watch deadline `2026-11-25 20:00 UTC`; planned air `Thu 26 Nov 12:00 London`)
- **Spend / mutations:** `£0.00` (zero YouTube/Studio writes, zero Buffer writes, zero NAS writes, zero generation)
- **Capabilities note:** Verified via exact file SHA-256 checks, `ffmpeg`/`ffprobe` full decode, loudness/silence/frame-difference measurements, `captions.ass` vs locked `ww2_001_en-GB.srt` audit, `ARCHIVE_PROVENANCE.md` verification, and direct visual inspection of `review_sheet.jpg` plus 14 full-resolution (`1080x1920`) extracted frames. No audio listening or moving-video perception is claimed; Ben's UAT supplies watch/listen (`AGENTS.md`).

---

## Verdict: **FIX** (Rebuild to `v02` at £0.00 before Ben's watch)

Do **not** register `v01` on Ben's watch card yet. With `>25 hours` remaining before Ben's `Wed 25 Nov 20:00 UTC` watch deadline and `~42 hours` before the `Thu 26 Nov 12:00 London` slot, a clean `£0.00` rebuild to `v02` (reusing the exact locked body VO, already-generated 94-character pickup VO, and already-cleared NAS assets) takes ~15 minutes on the Mini and resolves three visible defects that would otherwise ship in Field Order History's first-ever Short and propagate into the `J3563` template for films `002-010`.

> **Authority note:** `J3542` carries a structured hold (`scripts/jobs.py` restricts `reopen` of held jobs and PR merges to the elected Chief). This review leaves `J3542` untouched and queues an immediate elected-Chief follow-on job so the Chief can review this verdict, merge this PR, and reopen `J3542` immediately rather than waiting for the `2026-11-25T00:01Z` hold recheck.

---

## What Passed on `v01` (Keep Unchanged in `v02`)

1. **Container, codec, decode & duration:** `1080x1920`, `25 fps`, H.264 High `yuv420p`, `47.40 s` (`1185` frames), `ffmpeg -v error -i ... -f null -` exit `0` (`DECODE_OK`). Inside `J3542`'s `45-60 s` brief and WW2 `studio/RULES.md` Rule 1 (`under a minute`).
2. **Loudness & peak:** `-16.4 LUFS` integrated, `-1.5 dBFS` true peak, `3.8 LU` LRA (clean, non-clipping).
3. **Hook & narration:**
   - Question hook visible at frame 0 (`0.00-2.25 s`, *"How did the Mulberry harbours work?"*) and spoken `0.10-1.86 s` (under 2 s).
   - Body narration lifted verbatim from Pilot 1 locked VO (`588.40-628.90 s`), matching original pre-trim `ww2_001_en-GB.srt` (`09:48.520-10:28.780`).
   - Authorised 94-character pickup (`vo/mulberry_short_pickup_v01.mp3`, SHA-256 `0fe9d400a1371609d6d71453c31cbcbc894b1840b58ffe991fd7dafa3b1fab60`, `Ben Orbit Narrator` via `eleven_v3` API) verified in `stt_raw.json`: 17/17 spoken words matched (only UK/US `harbours`/`harbors` and `harbour`/`harbor` spelling difference). **Zero new VO spend needed for `v02`.**
   - Final line points cleanly to the full film (*"Watch the full D-Day harbour story on Field Order History"* + *"Tap the related video"*).
4. **Archive provenance, full-bleed & ad safety:**
   - All 5 source archive originals exist on the NAS with exact SHA-256 matches to `build_manifest.json` and are cleared official UK Crown-copyright-expired IWM or US Navy / Library of Congress public domain in `03_Picture/ARCHIVE_PROVENANCE.md`.
   - Full-bleed `9:16` throughout (zero blurred padding/letterbox bars, zero AI picture, zero Nazi insignia or graphic content).
   - Gentle camera motion verified on all 6 shots (none static: middle-frame `mean_abs_diff` `3.13-18.95` across shot intervals).
5. **Title & packaging:**
   - `Mulberry Harbours: How Did They Work?` (`37` chars `<= 50`, starts with exact searched name `Mulberry Harbours`, no vague/banned words, no exact collision; passes WW2 `studio/RULES.md` Rule 2 and Rule 13).
   - Zero YouTube/Studio mutations performed prior to Ben's OK.

---

## Blocking Issues Requiring `v02` Rebuild

### 1. Overlapping ASS Caption Cues Cause 14 Rendered Frames of Colliding/Garbled Text + 5 Mid-Sentence Shot-Cut Splits
- **Evidence:** `captions.ass` has **11 overlapping `Caption` cue pairs** (`0.02-0.06 s` overlaps), producing **14 rendered frames** at `25 fps` (`frames 95, 162, 201, 351, 384, 424, 589, 590, 610, 683, 684, 844, 989, 990`) where two `Caption` events draw simultaneously.
- **Visually confirmed collisions on full-resolution extracted frames:**
  - **Frame `162` (`6.48 s`):** renders `"five interlocking rings."` stacked directly over `"offshore, in eleven to"`, overwriting `"Furthest"` into garbled text.
  - **Frame `683` (`27.32 s`):** renders `"seabed. Flanking the"` stacked directly over `"wall in shallower water"`, overwriting `"concrete"`.
- **Mid-sentence shot-cut splits:** All 5 shot cuts (`6.07 s`, `13.47 s`, `26.29 s`, `33.13 s`, `39.21 s`) split an active caption cue across natural VO pauses (`0.60-1.40 s` measured via `silencedetect`), leaving the previous ring's text on screen over the next ring's photograph and label (e.g., `"steel Bombardons. One thousand"` stays up after the `13.47 s` cut to `2 / PHOENIX CAISSONS`; `"seabed. Flanking the concrete"` stays up after the `26.29 s` cut to `3 / GOOSEBERRIES`; `"ships called Gooseberries. Inside"` stays up after `33.13 s` to `4 / SPUD PIERHEADS`).
- **Minor text alignment:** `captions.ass` reads `"Furthest"` and `"Spud pier heads"` vs locked `ww2_001_en-GB.srt` `"Farthest"` (`09:52.220`) and `"Spud pierheads"` (matching Label `4 / SPUD PIERHEADS`).
- **Exact fix for `v02`:** Enforce strict non-overlapping `Caption` timestamps (`prev.end <= next.start`, minimum `>= 0.04 s` or exact frame-boundary handoff), break cues cleanly on sentence boundaries and shot cuts (`6.07 s`, `13.47 s`, `26.29 s`, `33.13 s`, `39.21 s`), and match `"Farthest"` and `"Spud pierheads"`.

### 2. Severe Upscaling (`3.20x-3.67x`) Violating Pilot 1's `2.35x` Cap + Exact Photo Duplication Across 40% of Runtime
- **Evidence:** Pilot 1's own `ARCHIVE_PROVENANCE.md` (line 19) caps archive enlargements at **`2.35x`**. Three of `v01`'s six shots blow past that cap and appear visibly soft/smeared at `1080x1920`:
  - **Shot 3 (`26.29-33.13 s`, `3 / GOOSEBERRIES`):** `A_24159_25266765.jpg` (`800x523`, cropped to `294x523`) upscaled **`3.671x`** — visibly smeared silhouette strip with ~85% empty sky/water in full-res frame `29.8 s`.
  - **Shot 4 (`33.13-39.21 s`, `4 / SPUD PIERHEADS`):** `IWM_H_39297.jpg` (`800x557`, cropped to `313x557`) upscaled **`3.447x`** — visibly soft in full-res frame `36.5 s`, even though Pilot 1's NAS already holds cleared high-res **`03_Picture/archive_v43/80_G_285141.jpg` (`2662x2142`, US Navy / NARA Spud pierhead towers & Whale span — ~`0.90x` native scale, zero upscaling)**.
  - **Shot 1 (`6.07-13.47 s`, `1 / BOMBARDONS`):** `A_25814_25084644.jpg` (`800x600`, cropped to `337x600`) upscaled **`3.200x`** — noticeably soft with ~45% overexposed blank sky in full-res frame `8.5 s`.
- **Shot 0 / Shot 2 duplication (`40%` of runtime on one photo):**
  - Shot 0 (`0.00-6.07 s`) and Shot 2 (`13.47-26.29 s`, `12.82 s` hold) use the **exact same photo** `B_5726_30887292.jpg` shifted only `36 px` horizontally (`x=217` vs `x=253`), covering `18.89 s / 47.40 s` (`39.9%`) of the Short.
  - Meanwhile, Pilot 1's NAS `03_Picture/` already holds cleared high-res originals for both the overview open and a split 2-shot Phoenix sequence:
    - Overview open (`0.00-6.07 s`): `archive_originals_v07/A_24675_25086141.jpg` (`2480x1673`, operating Mulberry B overview) or `archive_originals_v07/BU_1024_24494355.jpg` (`4580x4590`, Arromanches harbour aerial).
    - Phoenix caissons (`13.47-26.29 s`, split into two ~`6.4 s` shots): keep `B_5726_30887292.jpg` (`1789x1772`, `1.084x`) for the sunken spine wall (`~19.5-26.29 s`) paired with `archive_v42/IWM_H_39300.jpg` (`2746x2480`, towed Phoenix) or `archive_v43/IWM_H_38675.jpg` (`1868x1772`, completed Phoenix caissons) or `archive_v41/IWM_H_37606.jpg` (`3496x3508`, hollow concrete boxes under construction) for `13.47-19.5 s`.
- **Exact fix for `v02`:**
  1. Replace Shot 4 (`IWM_H_39297.jpg`, `3.447x`) with NAS `03_Picture/archive_v43/80_G_285141.jpg` (`2662x2142`, US Navy / NARA, `<= 1.0x`).
  2. De-duplicate Shot 0 and Shot 2 (`B_5726`) and split the `12.82 s` Phoenix hold into two distinct high-res shots (`<= 1.2x` upscale) using the cleared NAS originals above.
  3. Bring Shot 1 (`1 / BOMBARDONS`) and Shot 3 (`3 / GOOSEBERRIES`) inside `<= 2.35x` upscale without blurred padding: for Gooseberries, use cleared high-res NARA `80-G-285123` (`2941x2224`, cleared in `ARCHIVE_PROVENANCE.md` line 8 / `v41` line 134, if available on the Mini) or a clean native `9:16` code schematic showing the ring position beside the harbour (WW2 `studio/RULES.md` Rule 1 & Rule 5 explicitly permit code diagrams alongside `>=50%` real archive photos); for Bombardons (where only `800px` IWM scans `A_25814`/`A_23738` exist in Pilot 1), use a clean native `9:16` code schematic of the outer floating breakwater ring or a clean archival card framing inside `<= 2.35x` (no blurred-copy padding), keeping real archive photos `>= 65%` of total runtime.

### 3. YouTube Shorts Mobile UI Safe-Zone Collision on Credit and Lower Caption
- **Evidence:** In `captions.ass`, `Credit` uses `Alignment=1, MarginV=230` (bottom-left `y ≈ 1660-1690` of `1920`, only `12%` above the bottom edge) and `Caption` uses `Alignment=2, MarginV=335` (`y ≈ 1450-1585`).
- On YouTube Shorts mobile playback, the bottom `~380-420 px` (`20-22%`) is occupied by the channel handle, Subscribe button, title, progress bar, and the **Related Video pill** (which this Short's closing caption explicitly instructs viewers to tap). At `MarginV=230`, the archive credit sits behind YouTube's bottom chrome, and 2-line captions at `MarginV=335` crowd the Related Video pill.
- **Exact fix for `v02`:** Raise `Caption` to `MarginV=520` (centered safely clear of the bottom `420 px` chrome and `170 px` right button rail) and place `Credit` cleanly clear of bottom chrome (either top-aligned directly under `Label` at `MarginV=325`, or bottom-left at `MarginV=430` above the UI bar).

---

## £0.00 Polish Improvements to Include in `v02`

4. **Gentle Pilot 1 music bed (eliminates `1.40 s` and `1.17 s` digital dead silence):** `mulberry_short_v01.mp4` is dry voice-only, leaving `-inf dBFS` digital silence for `1.40 s` (`24.84-26.24 s`) and `1.17 s` (`46.24-47.40 s`), plus `0.60-0.75 s` silent gaps between rings. Mix Pilot 1's own already-owned score bed from the NAS (`05_Music/original_score_v01/engineering_v01.mp3`, `£0.00`) softly under the VO (`-16` to `-18 LU` below VO, faded cleanly over the last `1.0 s`) while keeping integrated loudness around `-15` to `-16 LUFS` and true peak `<= -1.0 dBFS`.
5. **Standard `48 kHz` AAC audio:** Resample the mix to standard `48000 Hz` stereo AAC (`192 kbps`) instead of `96000 Hz` (inherited from `voice.wav` `192000 Hz`).

---

## Publishing Handoff & Watch-Card Readiness Notes

- **Unpushed Mini branches:** `codex/J3542` (`e43f0d3`, WW2 repo) and `codex/J3542-ledger` (`c3129faa3e`, OWB repo) were not yet pushed to GitHub at review time (awaiting Claude Code's standing privacy-review & publish handoff on the Mini), so `VERIFICATION.json` and `CONTINUATION.md` on `codex/J3542` were not directly readable from remote git; all evidence here was verified directly against the exact finished master, `build_manifest.json`, `captions.ass`, `probe.json`, `loudness.txt`, `review_sheet.jpg`, pickup VO/STT, and NAS archive originals. Rebuilding `v02` onto `codex/J3542` lets Claude Code perform one single privacy-review & publish pass for the final cut.
- **Version preservation (`AGENTS.md` Never list):** Write the rebuilt cut as `Shorts/Mulberry_Test_v02/mulberry_short_v02.mp4` (leaving `Mulberry_Test_v01/` untouched on the NAS).
- **Exact Ben watch-card specification (once `v02` passes review, or if elected Chief overrides to KEEP `v01`):**
  - Register a dedicated Short watch card (e.g. `WW2:001-S1`, `--type short`), preserving the live long's existing `WW2:001` (`ek9F61FVYqY`) card.
  - Watch version: `v02` (after rebuild), watch deadline `2026-11-25 20:00` London, planned air `2026-11-26 12:00` London.
  - Title: `Mulberry Harbours: How Did They Work?` (`37` chars).
  - After Ben's OK: capture Pilot 1 (`ek9F61FVYqY`) Shorts/Related traffic baseline before release, upload Private, set `Related video = ek9F61FVYqY`, schedule `Thu 26 Nov 12:00 London`, and queue the 7-day read logged in `ww2-channel` `studio/LEARNINGS.md`. Nothing airs before Ben's OK.
