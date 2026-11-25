# J3647 — Independent Rule-H Review & Acting Chief Ruling: `WW2:004-S1` v01 (`J3570`)

- **Reviewer / Elected Acting Chief:** `gemini` (Gemini 4 Neon (High); verified via `scripts/chief_relay.py status`: `Chief: Gemini` under Ben's 24 Nov 2026 chain `Claude -> Codex -> Gemini -> Grok`; `claude` out of usage until `2026-11-25T07:50:00Z`, `codex` out of usage until Nov 27 / retry `02:41:22Z`)
- **Reviewed at:** `2026-11-25T02:04–02:11Z`
- **Short:** `WW2:004-S1` — *Mark 14 Torpedo: Why It Ran 10 Feet Too Deep* (`44` chars `<= 50`, WW2 `studio/RULES.md` Rule 2)
- **Parent film:** `WW2:004` — *Mark 14 Torpedo: Why Perfect Hits Failed* (`40` chars, airs `Tue 1 Dec 2026 17:00 London`)
- **Target air slot:** `Mon 30 Nov 2026 12:30 London` (`2026-11-30T12:30Z`) · **Ben watch due:** `Sat 28 Nov 2026 18:00 UTC` (`2026-11-28T18:00Z`)
- **NAS master:** `/Volumes/data/studio-live/ww2/02_Video-Projects/004_Why-US-Submarine-Torpedoes-Failed-21-Months/Shorts/004_S1_v01/mark14_depth_short_v01.mp4`
- **Exact Master SHA-256:** `fef4e0566ece342650cf4501a50f04042372cdad21be94b90740971b9b68e2e8` (`25,815,067` bytes)
- **Parent build job / PR:** `J3570` / `ww2-channel` PR #117 (`macbook/J3570`, merged to `main` at `4f2f42a3203e4d62c21da52253a3e534881c502d`)
- **Spend / external mutations:** `£0.00` (zero new voice, zero paid stock, zero YouTube/Studio uploads or schedule changes, zero Buffer writes)
- **Media perception note:** Genuine audiovisual review performed directly on `mark14_depth_short_v01.mp4` via `read_file` (`audio_input` + `moving_video_input`, confirmed both by fresh relay probe at `2026-11-25T01:34:11Z` and direct playback in this session: full British narration heard word-for-word `00:00–00:48` with music bed fade, plus 1 fps timeline frames) alongside direct visual inspection of `review_sheet.jpg` and 10 full-resolution (`1080x1920`) extracted frames covering frame 0 hook, all 5 archive photos, all 3 schematics, and the end card. Ben's final UAT watch remains required before any upload or publish.

---

## Verdict: **KEEP** (Merged `ww2-channel` PR #117 and Staged Dedicated Short Ben Watch Card `WW2:004-S1`)

All Rule-H technical, visual, audio, provenance, caption, packaging, and ad-safety checks **PASS**. As elected Acting Chief (`chief_relay.py status` re-checked before protected calls), I merged `ww2-channel` PR #117 (after cleanly resolving its `status.json` conflict against `J3639`'s `main` without altering `WW2:004`'s long-film watch state), delivered a checksum-verified private copy to `WW2 UAT/`, uploaded `ww2-004-s1-v01` to the private R2 watch store, and armed Ben's dedicated Short watch card **`WW2:004-S1`** (preserving long card `WW2:004` on `J3430`).

No YouTube upload, schedule, or public action is taken before Ben's watch OK.

---

## Independent Verification Checklist

1. **Exact NAS Master & Container Integrity — PASS**
   - `shasum -a 256` on NAS master: `fef4e0566ece342650cf4501a50f04042372cdad21be94b90740971b9b68e2e8` (`25,815,067` bytes, exact match to `VERIFICATION.json`, `manifest.json`, and PR #117).
   - `ffprobe`: `1080x1920`, H.264 (`yuv420p`), `25/1` CFR (`1215` frames, `48.600000 s` `< 60 s`), `48000 Hz` stereo AAC (`191.7 kbps`).
   - Full decode: `ffmpeg -i ... -f null -` decoded all `1215` frames with exit code `0`.
   - Mobile streaming `faststart`: MP4 box inspection confirmed `moov` atom at offset `32` (`38,085` bytes) ahead of `mdat`.

2. **Direct Audiovisual & Loudness Review — PASS**
   - `ebur128` + `silencedetect`: integrated loudness **`-16.6 LUFS`**, LRA **`4.6 LU`**, true peak **`-1.5 dBFS`**, **`0`** stretches `> 0.5 s` below `-60 dBFS`.
   - Direct listening via `read_file` on `mark14_depth_short_v01.mp4`: clear British narration (`Ben Orbit Narrator`, lifted from locked `submarine_torpedoes_vo_v01.wav`, `£0` new voice) matches every caption cue verbatim from `00:00` (*"Torpedoes were fired into nets."*) through `00:45` (*"...where he had told it to go."*). The `0.36 s` join between Seg A and Seg B around `16.04 s` (*"...and measured the result. The Bureau eventually confirmed the problem."*) sounds completely natural with zero splice clicks, distortion, or clipped consonants. WW2:004's own Cue 02 dark atmospheric score bed sits cleanly under the voice and fades out smoothly across the `2.48 s` end card (`46.12–48.60 s`).

3. **Caption Frame Invariants & British English — PASS**
   - Independently verified all `32` cues in `caption_frames.json` against `manifest.json` shot boundaries (`0, 186, 303, 401, 524, 645, 822, 966, 1153, 1215`):
     - **`0`** overlapping frame intervals (`prev.end <= next.start` everywhere).
     - **`0`** cues crossing any of the 8 shot boundaries.
     - **`0`** 1-word orphan cues.
     - British English confirmed (`first`, `metres`; schematic reads `ABOUT 3 METRES DEEPER`).

4. **Archive Share, Provenance, Upscale & Honest Context — PASS**
   - Real archive runtime: `734 / 1215` frames = **`60.41%`** of full `48.60 s` runtime (**`63.66%`** of `46.12 s` story runtime before the `2.48 s` end card), comfortably above WW2 `studio/RULES.md` Rule 1 (`>= 50%`).
   - All `5` unique US Navy / NARA RG 80 public-domain originals verified byte-for-byte on NAS `03_Picture/archive/` against both `manifest.json` and `03_Picture/HARVEST_LEDGER.md` / `ARCHIVE_PROVENANCE.md`:
     - `n01_nara_520831_torpedo_transfer.jpg` (`NARA 80-G-468128`): `f120e39f860b59d5e360608cf0b98f74f82aa011ff888cf15d6b93137da8137d` (`1.1026x` max upscale with 2.5% KB push)
     - `n03_nara_520832_torpedo_shop.jpg` (`NARA 80-G-468134`): `087fdf07ba7e9501fe6a0eaa9cd3e38e0739d2af04ecde5115818654f92d1c5e` (`0.8502x`)
     - `n08_nara_520846_new_london_bridge.jpg` (`NARA 80-G-468312`): `cc30ae5fac00363521e5b0afe3fc7d45efd58bd6c8128b579162ad1426965d6b` (`1.0583x`)
     - `n11_nara_520847_new_london_deck.jpg` (`NARA 80-G-468316`): `d49ccfd4eeabc0e0d5b423dbe48a8e79cd36e7ec2a8431adf3ecad1df223d86f` (`1.0197x` recomputed / `1.0193x` manifest)
     - `n07_nara_520588_periscope.jpg` (`NARA 80-G-11258`): `f475268160b5ea0d7b0e719baea4b9212686609575170d5f224c7808fc4e4df9` (`0.8450x`)
   - Maximum upscale **`1.1026x`** (well under `2.35x` cap), full-bleed `9:16` throughout with zero blurred padding and zero film/scanner borders.
   - Honest context per `HARVEST_LEDGER.md`: no photo is misattributed to *Tinosa*, Daspit, *Cero*, David White, exercise heads, or combat-loaded warheads; `metadata.json` explicitly notes general submarine/torpedo handling context, studio-drawn non-scale schematics, Rowland & Boyd (1953) pp. 97–99, and AI voice disclosure.

5. **Full-Resolution Visual & Mobile Safe-Zone Inspection — PASS**
   - Inspected `review_sheet.jpg` and 10 full-resolution (`1080x1920`) frames (`0.0 s`, `0.6 s`, `9.5 s`, `14.0 s`, `18.5 s`, `23.0 s`, `29.5 s`, `35.5 s`, `42.5 s`, `47.4 s`):
     - **Frame 0 hook (`0.0 s`):** sharp full-bleed `NARA 80-G-468128` torpedo hoist with clean yellow `MARK 14 TORPEDO: 10 FEET TOO DEEP` header + `US Navy / NARA 80-G-468128` credit clearly legible.
     - **Three FOH code schematics (`1942 NET TEST`, `10 FEET DEEPER`, `BENEATH THE KEEL`):** crisp dark-navy engineering style (`mean luma 42.64–46.76`), clearly marked `Studio schematic | not to scale`, citing `Rowland & Boyd, Bureau of Ordnance (1953), pp. 97-99 / p. 99`, using only spoken figures (`10 FEET` / `ABOUT 3 METRES DEEPER`, `10 FT`), zero overlapping elements (`TORN HOLE` inside the red ring is cleanly readable, though `T`/`E` kiss the ring edge slightly — minor cosmetic note only, non-blocking).
     - **End card (`46.12–48.60 s`):** clean FOH dark-navy card pointing to exact locked long title *Mark 14 Torpedo: Why Perfect Hits Failed* on Field Order History with *Tap the Related Video below* prompt.
     - **Mobile safe zones:** all top headers, credits, schematics, captions (`y <= 1390`, `MarginV >= 530`), and end card stay cleanly centered in the left `900 px` clear of YouTube Shorts bottom chrome and right button rail.
     - **Packaging & Ad Safety (Rules 2 & 13):** 44-char search-first title (`Mark 14 Torpedo: Why It Ran 10 Feet Too Deep`), hard number (`10 Feet`), zero Nazi insignia, zero graphic imagery, zero shock words.

---

## Acting Chief Actions Executed (`gemini`, 2026-11-25)

1. **PR #117 Hygiene & Merge (`ww2-channel`):**
   - Hygiene-scanned all 8 PR #117 files: zero secrets, tokens, emails, or private IPs.
   - Resolved the `02_Video-Projects/004_Why-US-Submarine-Torpedoes-Failed-21-Months/status.json` merge conflict against `origin/main` (`J3639`) in commit `ffadab3`, preserving `WW2:004`'s long-film watch state intact while recording `004-S1` as `staged_for_ben_watch` (`watch_id: ww2-004-s1-v01`, `watch_card: WW2:004-S1`).
   - Merged `ww2-channel` PR #117 cleanly to `main` at **`4f2f42a3203e4d62c21da52253a3e534881c502d`**.
2. **Checksum-Verified Private Ben Watch Staging (No Upload):**
   - Copied exact NAS master to iCloud `WW2 UAT/004_Why-US-Submarine-Torpedoes-Failed-21-Months/Shorts/004_S1_v01/mark14_depth_short_v01.mp4` and verified byte-for-byte SHA-256 `fef4e0566ece342650cf4501a50f04042372cdad21be94b90740971b9b68e2e8` (`25,815,067` bytes).
   - Uploaded private watch stream `watch/ww2-004-s1-v01/6f60a78b26357a17-mark14_depth_short_v01.mp4` (`ww2-004-s1-v01`) to private R2 watch bucket and registered both iCloud and NAS paths in local `~/.config/studio-kanban/watch_uploads.json` and repo `05_Analytics/kanban/watch_uploads.json`.
   - Armed dedicated Short Ben watch card **`WW2:004-S1`** on `J3570` (`due 2026-11-28T18:00Z`, `airs 2026-11-30T12:30Z`, `type: short`), preserving long card **`WW2:004`** on `J3430` untouched, and verified via `board_publish.py` + `board_check.py`.
