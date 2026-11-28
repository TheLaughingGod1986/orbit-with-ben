# J3643 — QA Verification of `WW2:003` (`v01`, B-29 Superfortress) & Ben Watch Handoff

- **Reviewer:** `gemini` (dispatched on `qa` lane by relay while `claude`, `claudecode`, `codex`, and `cursor` are out of usage)
- **Independence disclosure:** `gemini` also completed the final `J3205` assembly run (`codex/J3205-mini`, `4d8422d`) after `codex` staged the earlier passes. Every measurement, hash, decode, caption diff, provenance audit, visual frame sheet, cover check, and direct A/V perception below was freshly executed from scratch against the exact NAS master and phone proxy. No YouTube upload, no scheduling, and no bypass of Ben's watch or returning-Chief final sign-off occurred.
- **Reviewed at:** `2026-11-24T23:38–23:45Z`
- **Target master:** `ww2/02_Video-Projects/003_Why-B29-Superfortress-Cost-More-Than-Atomic-Bomb/07_Edit/v01/ww2_003_b29_superfortress_v01.mp4` on the NAS
- **Master SHA-256:** `876736a1a23d42109a5648bb7188707f842843c15dcd1a3d882de4dd8a027a66` (`381,034,590` bytes)
- **Phone proxy SHA-256:** `7e105c11e6219a0372010d21ff2ba3f493dfa265a4b70ccbb733d0c785ff38ac` (`170,239,867` bytes)
- **Private board watch stream:** `ww2-003-v01` uploaded from the verified NAS `720p30` phone proxy (`170,239,867` bytes) via `scripts/watch_upload.mjs`
- **Ben watch card:** Set on `J3205` (`WW2:003`, `v01`, due `Wed 25 Nov 20:00 UTC`, planned air `Sat 28 Nov 17:00 London`)
- **Spend / mutations:** `£0.00` (zero YouTube/Studio writes, zero Buffer writes, zero generation)
- **Capabilities & perception:** Freshly demonstrated `audio_input` and `moving_video_input` via direct inspection of extracted moving A/V clips (`00:00–00:12`, `00:36–00:48`, `25:38–25:50`) in addition to full-file `ffmpeg`/`ffprobe`/SHA-256/SRT/provenance checks and four fresh visual contact sheets archived on the NAS (`07_Edit/v01/qa_j3643/`).

---

## Verdict: **PASS FOR BEN'S PRIVATE WATCH (`v01`)**

Every technical, caption, archive provenance, Rule 1/2/3/5/13, graphic, cover, and A/V sync check passed with zero blocking defects. `ww2-003-v01` is uploaded to the private board watch bucket and `WW2:003` (`v01`) is placed on Ben's UAT watch card due **Wed 25 Nov 20:00 UTC** (planned air **Sat 28 Nov 17:00 London**).

---

## Fresh Verification Results

1. **Exact hashes & streams:**
   - Master (`1920x1080`, `30 fps`, H.264 High `yuv420p`, `46,509` frames, `1550.298 s` video / `1550.293 s` audio, `48 kHz` stereo AAC `191 kbps`, `381,034,590` bytes): SHA-256 `876736a1a23d42109a5648bb7188707f842843c15dcd1a3d882de4dd8a027a66` verified.
   - Phone proxy (`1280x720`, `30 fps`, H.264 High `yuv420p`, `46,505` frames, `1550.293 s` container, `48 kHz` stereo AAC `191 kbps`, `170,239,867` bytes): SHA-256 `7e105c11e6219a0372010d21ff2ba3f493dfa265a4b70ccbb733d0c785ff38ac` verified.
   - Note on iCloud UAT copies: macOS evicted the iCloud copies to `compressed,dataless` placeholders matching exact byte sizes (`381,034,590` and `170,239,867` bytes); `watch_upload.mjs` uploaded the verified NAS `_PHONE.mp4` directly.
2. **Full decode, loudness, peak, black & silence:**
   - `ffmpeg -v error -i <master> -f null -` -> exit `0`, **`0` decode errors**.
   - Fresh `ebur128=peak=true`: Integrated **`-16.3 LUFS`**, LRA **`4.4 LU`**, True Peak **`-1.8 dBFS`** (zero clipping).
   - Fresh `blackdetect=d=0.5:pix_th=0.10`: **`0`** intervals.
   - Fresh `silencedetect=noise=-45dB:d=2.5`: **`0`** intervals.
3. **Captions against locked narration (`11_Upload-Package/ww2_003_en-GB_v01.srt`):**
   - SHA-256 `8836e6472e1cf360a231be7a37d9269dcc253f4350b8f9cb436c8935af9dbe7a` matches `metadata_v01.json`.
   - **`401` cues** (`0.16 s`–`1550.38 s`), **`0` overlaps**, **`0` malformed/bad-duration cues**, **`0` lines > 48 chars**.
   - **`3,501 / 3,501` words** matched against locked `v04` Scribe STT (`0.9957` raw similarity; all `15` diff hunks are intentional UK/US orthography conversions: `aeroplane`, `pressurised`, `calibre`, `analogue`, `programme`/`programmes`, `harbour`, `centres`, `labourers`).
4. **Archive share, provenance & ad safety (Rules 1, 5, 13):**
   - Independent recalculation of `EDIT_PLAN_v11.json` (`74` shots, `1550.42 s`): **`61.38%`** pure archive (`951.635 s` across `40` unique US federal PD photographs, Rule 1 floor `>=50%`), **`38.62%`** code-drawn maps/diagrams (`598.785 s`, `27` full-duration renders).
   - **`40 / 40`** NAS archive files verified with exact SHA-256 matches to `03_Picture/ARCHIVE_PROVENANCE.md`; **`0`** excluded/flagged photos present in `EDIT_PLAN_v11.json`.
   - Minimum archive repeat gap **`102.8 s`** (`0` repeats `< 60 s`). Maximum full-frame cover upscale **`2.177x`** (`<= 2.35x`).
   - Rule 13 ad-safety: zero Nazi insignia, zero bodies/executions/atrocities across all inspected frames and launch covers.
5. **First two minutes against Rule 3 (independent 26-frame sheet `first_2min_sheet.jpg` + direct A/V clips):**
   - Concrete moment inside 30 s: `00:00–00:22` compares `$1.9 billion` Manhattan Project vs `$3 billion` B-29 with animated cost bars, cutting at `00:22.92` to silver B-29 in flight (`A01a`).
   - Promise by 45 s: `00:23–00:46` establishes that America's most expensive weapon did not work as meant, launching at `00:38.62` into the Seattle XB-29 crash killing 32.
   - Main story moving by 1:00: `00:47–01:33` introduces R-3350 magnesium fires, Kansas snowbound fleet, 200 mph jet stream, and the 1,600-bomber pre-first-flight gamble without answering the title; `01:34` begins Chapter 2 (1939 Hap Arnold & Pacific range map).
   - Zero channel intro, zero "in this video"; all 7 chapters (`00:00`–`22:43`) match exact shot starts in `EDIT_PLAN_v11.json` and `DESCRIPTION_v01.txt`.
6. **All 27 graphics, full-runtime spot sheet & direct moving A/V check:**
   - Inspected all 27 rendered graphics (`all_27_graphics_sheet.jpg`) and 24 full-runtime spot frames (`full_runtime_spot_sheet.jpg`): clean typography, UK spelling, zero overlaps, zero clipped labels, zero internal job IDs.
   - Direct A/V inspection of `00:00–00:12`, `00:36–00:48`, and `25:38–25:50` confirmed crisp narration, balanced subtle music bed, smooth camera/graphic motion, and zero A/V drift through the final sentence (*"...Fifi and Doc, still fly today"*).
7. **3 launch covers at `168x94` px & title (Rules 2, 13):**
   - All 3 NAS covers (`1280x720`) match `metadata_v01.json` SHA-256s: `A` (`$3 BILLION`), `B` (factory close-up, no text), `C` (`ENGINE FIRES`).
   - Verified at `168x94` with simulated `25:50` bottom-right duration badge (`covers_168px_sheet.jpg`): single bold archive subject per cover, sharp top-left text on solid dark band (0–2 words), zero duration-badge collision, Rule 13 clear.
   - Title `B-29: Why It Cost More Than the Atomic Bomb` (`43` chars `<= 50`, starts with searched name `B-29`, Rule 2 & Rule 13 PASS).

---

## Publish Handoff

- **WW2 local branches (for Claude Code privacy review & push, in order):**
  1. `codex/J3205-mini` (`4d8422d`) — J3205 v01 assembly, provenance & upload package
  2. `gemini/J3643-qa` — this J3643 QA verification record
- **OWB local branch (for Claude Code privacy review & push):**
  - `gemini/J3643-review` — `jobs/reviews/J3643/REVIEW.md`, `EVIDENCE.json`, and `05_Analytics/kanban/watch_uploads.json` (`ww2-003-v01`)
- No YouTube upload or schedule occurs until Ben approves `v01` on his watch card.
