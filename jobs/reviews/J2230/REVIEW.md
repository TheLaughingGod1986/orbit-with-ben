# J2230 — Elected Acting Chief Ruling (`HOS:005`, `HOS:006`, `HOS:007` Late-November Shorts Gap)

- **Job:** `J2230` (`HOS Shorts gap after 17 Nov: cut six search-titled Shorts from the locked Harvey, Willow and Vaccine longs, slot 18 Nov to 6 Dec`, `repo: hos`, `needs: mini`, `kind: assembly`)
- **Elected Acting Chief:** `gemini` (`Gemini 4 Argon (High)`, elected acting Chief for both OWB (`Claude -> Grok -> Codex -> Gemini`) and HOS (`Grok -> Claude -> Codex -> Gemini`), verified via `python3 scripts/chief_relay.py status` at `2026-11-14T11:46:47Z`)
- **Capabilities Demonstrated:** `audio_input` (verified via direct `read_file` playback on `/Users/benjaminoats/_desk/renders/J2230/eradication_corrected_inputs_v02/eradication_vo_from_master_v02.wav` plus prior full-sample listening in `cc9c5bef`), still-frame/contact-sheet visual review (`picture_qa_review.jpg`, `hos_005_s06_blood_pressure_cuff_v02_open_sheet.jpg`, `hos_005_s07_heart_pulse_v02_open_sheet.jpg`), and current `gate_shorts_open.py check` runs.
- **Spend & Public State Changes:** **£0 / 0 credits.** No ElevenLabs TTS or video/image generation authorized. No YouTube upload, schedule, or `jobs.py awaits` until the four remaining cuts (`2` Harvey + `2` Vaccine) pass all current gates and QA.

---

## 1. Evidence Reviewed

1. **HOS PR `#559` (`cc9c5bef`, merged to HOS `main`) & `jobs/J2230/GEMINI_AUDIO_AND_SLOTS_2026-11-12.md`:**
   - Direct listening on `eradication_vo_from_master_v02.wav` (`sha256: 388ae394a55e0d850bcf40a4ad73105b517e13814d8e113e665f50dfbc2a4963`), `eradication_vo_input_v02.wav` (`sha256: 19ee3cedf52dd802a77bf1634407a6bc5daff848be7f016de705e9b25f97c4a3`), and raw locked Part 05 (`part05_the_word_that_saved_millions_v01b.mp3`, `sha256: 18b725326c0b40e6bba2250be9f25a2581366a2ff76a2121fa889191f727557f`) confirmed two real defects in the v02 Eradication stem:
     - `0:00–0:03` (`41.38–42.65 s` raw Part 05): narrator speaks **"A disease that have killed hundreds of millions..."** (real spoken `/v/` in `"have killed"`, not `"had killed"`), and opens on `"A disease"` without naming `smallpox` in sentence 1 (`LEARNINGS.md` rules 8 & 24).
     - `0:06–0:09`: the `49.10 s` trim chops off the final `/z/` of `"humans."` (`48.30–49.35 s` raw) and butt-splices into `"Health workers"` with zero breath.
   - Direct listening on `variolation_vo_input_v01.wav` (`sha256: cdf6e02772fc244fcc7d944ca7a75a136a5bedeb6f6050abfc925e53a3bad767`, `24.50 s`, 61 words from `part01_the_speckled_monster_v03.mp3` `3881da7b…` `[67.66, 92.16]`) confirmed clean speech throughout (*"Doctors took a little matter from a smallpox sore and scratched it into a healthy person's arm..."*).
   - Direct listening on Harvey `005` `hos_005_s07_heart_pulse_v02.mp4` (`sha256: 51a4b10d74ae0981c8dfc66e59696f3174802ef6da5c2697861dbce877970703`, `25.10 s`) and `hos_005_s06_blood_pressure_cuff_v02.mp4` (`sha256: 8ac9a2917a9842a872131554ad0c898df69fc226dae193a94f9195d9b8baa888`, `23.10 s`) cleared both audio flags by ear (`vo_check` `"it circulates"` insert at `~0:24.22` on `s07_v02` is an ASR false positive over the quiet instrumental tail; `music_gate` `~150 BPM` warning on `s06_v02` is double-time detection on a calm plucked bed).
2. **2026-11-14 HOS YouTube Snapshot (`05_Analytics/hos/snapshots/2026-11-14.json`) & `00_Brand/Channel-Setup/social/hos/UPLOADS.json`:**
   - **Parent longs are all PUBLIC:**
     - `005` Harvey (`wwcjcFfC-5M`, *The Tied Arm That Proved Your Blood Circulates*) — Public since `2026-10-29T18:00:28Z`.
     - `006` Willow (`VbPubYd6Fbs`, *The Willow Tree That Was Made of Air*) — Public since `2026-11-05T18:00:17Z`.
     - `007` Vaccine (`ETynHpIYLeY`, ***How Was the First Vaccine Made? (And Why It's Named After a Cow)***) — **Public since `2026-11-12T18:00:36Z`**. (Note: live YouTube title is now `How Was the First Vaccine Made? (And Why It's Named After a Cow)`, superseding the 6 Nov pre-publish title `Why Vaccines Are Named After a Cow`.)
   - **Scheduled HOS Shorts after 17 Nov:**
     - `Wed 18 Nov 2026 11:30Z`: `ChbsigHD5_o` (*How Do Plants Clean the Air?*, `006` Willow Short B `J2272`).
     - `Sat 21 Nov 2026 11:30Z`: `Bks_JLId1ew` (*How Do Plants Make Oxygen?*, `006` Willow Short C `J2273`).
     - **10 of 11** locked 7 Nov HOS pattern slots (`Sat · Fri · Sun · Tue 11:30 London` in `18 Nov – 6 Dec`) remain empty on YouTube: `Fri 20 Nov`, `Sun 22 Nov`, `Tue 24 Nov`, `Fri 27 Nov`, `Sat 28 Nov`, `Sun 29 Nov`, `Tue 1 Dec`, `Fri 4 Dec`, `Sat 5 Dec`, `Sun 6 Dec`.
3. **Current `gate_shorts_open.py` & Visual Check on `s06_v02` and `s07_v02` (`origin/cursor/J2230-s07` `c8c8683c` / `2dbbb7dc`):**
   - Running `python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check` today (`14 Nov 2026`) **FAILS both `v02` files** built on 6 Nov:
     - `hos_005_s06_blood_pressure_cuff_v02.mp4`: `FAIL missing on-screen hook text at frame 0 (hook_edge 0.0004 < 0.005) — stamp 2–4 word hook caption at 0.0s` + `warn the picture does not fill 9:16 on 4/47 sampled frames: 2-2s (blur-pad, no edge), 15-16s (blur-pad), 23-24s (blur-pad, no edge)`.
     - `hos_005_s07_heart_pulse_v02.mp4`: `FAIL missing on-screen hook text at frame 0 (hook_edge 0.0009 < 0.005) — stamp 2–4 word hook caption at 0.0s` + `warn the picture does not fill 9:16 on 2/51 sampled frames: 4-4s (mirror), 10-11s (blur-pad)`.
   - Inspecting the open sheets (`hos_005_s06_blood_pressure_cuff_v02_open_sheet.jpg` and `hos_005_s07_heart_pulse_v02_open_sheet.jpg`) confirms why: both `v02` builds placed their 2-word hook (`THE CUFF`, `YOUR PULSE`) dead-centre (`block_pct: [39.5, 60.4]`) directly over the hero object (violating `studio/RULES.md` § *Packaging*: *"Lettering in a clear band (the top, or the live layout's left edge), never over the hero object"*) with thin stroke contrast over bright skin/red glow, missing `gate_shorts_open.py`'s `0.08..0.48 H` upper-middle hook band and `rgb <= 65` dark-stroke threshold (`hook_edge >= 0.005`). Both also retain padded/mirror stretches (`studio/RULES.md` Never list, 10 Nov 2026).

---

## 2. Chief Rulings

### Ruling 1 — Calendar & Willow (`006`) Pair
- **Willow `006` pair (`ChbsigHD5_o` on Wed 18 Nov 11:30Z and `Bks_JLId1ew` on Sat 21 Nov 11:30Z) counts as the two Willow Shorts for `J2230`.** Do not rebuild or duplicate Willow Shorts.
- **Target HOS pattern slots (`Sat / Fri / Sun / Tue 11:30 London`, Ben 7 Nov 2026) for the 4 remaining cuts (`2` Harvey + `2` Vaccine):**
  1. **Harvey `005` Cuff (`How Does a Blood Pressure Cuff Work?`)** → **Fri 20 Nov 2026 11:30Z** (or next open pattern slot after Ben's watch).
  2. **Harvey `005` Heart-Pump (`How Does the Heart Pump Blood?`)** → **Sun 22 Nov 2026 11:30Z** (on-pattern Sun, replacing pre-7-Nov Mon 23 Nov draft).
  3. **Vaccine `007` Variolation (`What Is Variolation?`)** → **Sat 28 Nov 2026 11:30Z** (on-pattern Sat; `ETynHpIYLeY` is already public).
  4. **Vaccine `007` Eradication (`How Was Smallpox Eradicated?`)** → **Sun 29 Nov 2026 11:30Z** (on-pattern Sun, or `Sat 5 Dec` / `Sun 6 Dec 11:30Z` if `009` Moon Short B occupies `Sun 29 Nov`).
  - Leave `Tue 24 Nov` (`008` Franklin Short A), `Fri 27 Nov` (`009` Moon Short A), `Tue 1 Dec` (`008` Short C), and `Fri 4 Dec` (`010` Alvarez Short A) clear for the upcoming longs' own Shorts.

### Ruling 2 — Vaccine `007` Eradication Short (`How Was Smallpox Eradicated?`): **Choose Option A (£0 Locked Part 05 Re-selection)**
- **Approved Option A (£0 / 0 credits, zero new generation):** Drop the defective `41.38–49.35 s` (`"A disease that have killed..."`) sentence completely and build from clean locked `part05_the_word_that_saved_millions_v01b.mp3` (`sha256: 18b725326c0b40e6bba2250be9f25a2581366a2ff76a2121fa889191f727557f`) intervals only:
  1. **Sentence 1 (`[35.16, 40.72]`, 16 words, tightening the raw `36.45 -> 37.42 s` internal pause after `"1980,"` to `0.20 s`):**
     *"On the eighth of May, nineteen eighty, the world's health leaders declared that smallpox was gone."* (Names **`smallpox`** in sentence 1 and eliminates the defective `"A disease that have killed..."` take.)
  2. **`+ 0.30–0.40 s` natural breath + Sentence 2 (`[25.36, 34.50]`, 25 words):**
     *"Health workers travelled to every country where smallpox still lived, vaccinating everyone around each new case, until there was nowhere left for it to go."*
  3. **`+ 0.30–0.40 s` natural breath + Sentence 3 (`[70.06, 75.70]`, 20 words, starting at `≥70%` of runtime per `LEARNINGS.md` rule 6):**
     *"And because no one alive today needs a vaccine against smallpox, most of us have never seen it at all."*
  - **Totals:** **61 words** (within the 55–65 word lock), `~21.0 s` speech + `<1.0 s` loop tail = **`~22.0–22.5 s`** total (within the 22–27 s lock), **£0**.
  - **YouTube Title:** `How Was Smallpox Eradicated?` (exact signed-out GB autocomplete hit).
  - **9–14 s Parent Long Banner:** Must use the exact current live YouTube title of `ETynHpIYLeY`: **`How Was the First Vaccine Made? (And Why It's Named After a Cow)`**.

### Ruling 3 — Vaccine `007` Variolation Short (`What Is Variolation?`): **Approve 61-Word Locked Part 01 Selection at £0**
- **Approved VO (`[67.66, 92.16]` from `part01_the_speckled_monster_v03.mp3` `3881da7b…`, 61 words, £0):**
  *"Doctors took a little matter from a smallpox sore and scratched it into a healthy person's arm. It usually gave a milder illness, and lifelong protection. It was called variolation. But some people died from it, and they could pass full smallpox on to others. So people faced a terrible choice. Risk the treatment, or wait for the monster to come."*
  - Tighten inter-sentence pauses (`73.35->74.10`, `77.45->78.28`, `79.60->80.96`, `85.20->86.26`) to `0.25–0.35 s` so total runtime with a `<1.0 s` loop tail lands around **`22.5–23.5 s`**.
  - **YouTube Title:** `What Is Variolation?` (verified signed-out GB autocomplete hit; `What Was Variolation?` had 0 suggestions).
  - **9–14 s Parent Long Banner:** **`How Was the First Vaccine Made? (And Why It's Named After a Cow)`**.

### Ruling 4 — Harvey `005` Shorts (`s06_blood_pressure_cuff` & `s07_heart_pulse`): **Audio Approved; Rebuild as `v03` (`£0`) to Pass Current `gate_shorts_open.py`**
- **Audio & VO stems (`v02`) are APPROVED by ear:** keep the exact `v02` VO trims (`vo_s: 22.542`, 59 words on `s06`; 64 words on `s07`) and music beds unchanged (`£0`).
- **Required `v03` visual fixes before QA / `jobs.py awaits`:**
  1. Move the frame-0 hook caption (`THE CUFF` on `s06_v03`; `YOUR PULSE` on `s07_v03`) into the **upper clear band (`~0.14–0.34 H`)**, off the hero cuff/heart, stamped at `t = 0.0 s` with high-contrast white + `#FFE000` yellow and dark stroke (`rgb <= 65`) so `gate_shorts_open.py` `frame0_hook_text_score` (`0.08..0.48 H`) scores `hook_edge >= 0.005` (`PASS`).
  2. Fix the remaining padded/mirror stretches (`2-2s, 15-16s, 23-24s` on `s06`; `4-4s, 10-11s` on `s07`) using full-bleed `9:16` (`mode: "cover"`, zero blur-pad/mirror bands) so `gate_shorts_open.py check` prints **PASS** with `0` fails and `0` padded stretches.

---

## 3. Concrete Next Steps (Reopened for `cursor` on `cursor-grok-4-7`, `kind: assembly`)

1. Re-cut Harvey `s06_v03` and `s07_v03` from existing `origin/cursor/J2230-s07` scripts (`_build_short_s06_blood_pressure_cuff_v02.py`, `_build_short_s07_heart_pulse_v02.py`) with top-band `0.0 s` hook text (`hook_edge >= 0.005`) and full-bleed `9:16` cover crops on all rows (`0` padded/mirror frames).
2. Assemble Vaccine `007` `What Is Variolation?` (`v01`) and `How Was Smallpox Eradicated?` (`v01`, Option A 61-word clean Part 05 recipe) in vertical `9:16` full-bleed (`mode: "cover"`), top-band `0.0 s` hook caption (`hook_edge >= 0.005`), one house-style teaching card/WHO card clear of `0–2 s` and `9–14 s`, exact live parent long title `How Was the First Vaccine Made? (And Why It's Named After a Cow)` at `9–14 s`, `<1.0 s` loop tail, and separate VO/music/SFX stems.
3. Run `vo_check.py` (on stems), `sfx_kit.py level`, `polish_gate`, `picture_qa`, `music_gate`, and `gate_shorts_open.py check` on all four cuts (`s06_v03`, `s07_v03`, Variolation `v01`, Eradication `v01`), copy verified masters to NAS / HOS UAT, and commit manifests + gate outputs via HOS PR before setting `jobs.py awaits`.
