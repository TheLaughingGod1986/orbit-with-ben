# J2687 — Condition Verification for J2662 (HOS 008 Short C v04 Re-cut Inputs)

- **Job:** `J2687` (`recheck_of`: `J2662`)
- **Verifier:** `gemini` (`gemini-argon`)
- **Verified at:** `2026-11-13T08:51:00Z`
- **Condition Verdict:** **`MET`** (all eight raw source clips and the `J2255` build recipe are present on the Mac mini and restored with 3-way SHA-256 verification to both the shared NAS working store `studio-live` and the Mini shared HOS checkout; all VO, STT, music bed, and house SFX inputs are verified intact; £0 spend).

---

## 1. Original Waiting Condition & Context (`J2662`)

`J2662` (*"HOS 008 Short C: re-cut hos_008_short_C_v04.mp4 for J2485 fix list (1.5 s surprise word, caption overlaps, S06/S07 offsets, S01/S02 crops, GBP0)"*, `repo: hos`, `needs: mini`, `film: 008`, `stage: edit`) was claimed by `macbook-2` on `2026-11-12` and parked with:

> `Missing raw media on studio-live: all eight v03 source clips absent. Resume on Mini originals or restore sources with SHA-256 checks before dispatching to MacBook again. Existing HOS PR #556 refreshed at 262ea41; v04 not rendered. Recipe recovered from open PR #555.`

Why the clips were missing on `studio-live`:
- In `J2255` (HOS PR [`#555`](https://github.com/TheLaughingGod1986/history-of-science/pull/555), commit `a0190a2f2af1f3296c8bc0d459dd1a506e8c4e9f`), `_build_short_c_v03.py` read its eight raw source plates from the Mac mini's dedicated HOS 008 picture checkout:
  `/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/`
- Those eight raw clips had not yet been copied into `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/` or `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/`.

---

## 2. Restoration & 3-Way SHA-256 Verification of All Eight Raw Source Clips

All eight `v03` raw source clips (`1280×720`, `24 fps`, `8.000000 s`) were verified in `/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/` and copied with byte-for-byte SHA-256 verification to:
1. **Shared NAS store (`studio-live`):** `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/`
2. **Mini shared HOS checkout:** `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/` (covered by `.gitignore:26:**/*.mp4`)

| Shot(s) in Short C | Relative Path under `04_Generated-Clips/` | Bytes | Duration | 3-Way Verified SHA-256 (`hos-008-lightning` = `studio-live` = `History Of Science`) |
|---|---|---:|---:|---|
| `S01`, `loop_tail` | `part05/raw/v01/19_skyline_strike_t1.mp4` | `4,806,014` | `8.000000 s` | `06caaeb6b7394ad590547b2f3f09db2dbe3a4a0354977591d36fb72769065026` |
| `S02` | `part05/raw/v01/01_house_rod_t1.mp4` | `3,220,554` | `8.000000 s` | `3822f6f706eb9263e2ec0fd6f3f8cb4b46bdb848778622505d25af1ad52001a3` |
| `S03` | `part05/raw/v01/07_giant_spark_t1.mp4` | `3,035,038` | `8.000000 s` | `8be031a332ec3ef63a3702a29f0df90230d7dec95ea27d0da83e90bd82c3c293` |
| `S04` | `part01/raw/v01/12_steeple_fire_t1.mp4` | `4,984,373` | `8.000000 s` | `421b96d9b6c6497bbae10abeaca56af50230c11fc2024988906429fbb0c6c453` |
| `S05` | `part05/raw/v01/18_rod_closeup_t1.mp4` | `1,933,863` | `8.000000 s` | `9535c72f68606a9de5293739535dd9b826ca624daf73889fa2aba46b5b36ce15` |
| `S06` (FIX 4: `4.00–6.792 s`) | `part05/raw/v01/06_rod_fitting_t1.mp4` | `2,057,993` | `8.000000 s` | `73c43fc2502c38dbbc8e65691402c6ee84e4937c429647f6270e2cc372fd38ad` |
| `S07` (FIX 3: `3.10–5.808 s`) | `part05/raw/v01/06_rod_fitting_c1_t1.mp4` | `3,574,606` | `8.000000 s` | `de605071ba81008eca11b7e10c17e9fcf88ac303f32d800c8fb745793d4f6908` |
| `S08` | `part05/raw/v01/14_safe_towers_t1.mp4` | `3,691,858` | `8.000000 s` | `0c7e98c2d89d2e4ef61271af00d71ae77d9e1e55b871b70bdc33ea79e81ffbdd` |

---

## 3. Build Recipe & Existing Audio/Master Inputs Verified (`studio-live` & Mini `shared`)

The `v03` build script from HOS PR `#555` (`a0190a2f2af1f3296c8bc0d459dd1a506e8c4e9f`) was also restored to `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/J2255/_build_short_c_v03.py`, and all existing audio/VO/music/SFX/master files match byte-for-byte between Mini `shared` and `studio-live`:

| Input Role | Relative Path under `02_Video-Projects/008_Lightning-Franklin/` | Bytes | Verified SHA-256 (`shared` = `studio-live`) |
|---|---|---:|---|
| Build recipe (`J2255`, PR `#555`) | `10_Shorts/J2255/_build_short_c_v03.py` (`studio-live` + git `a0190a2f`) | `13,803` | `0b59eb72e78407b21cb2150a695c27c17a0c8f9bca55752347fa1cef7034ffd6` |
| Sentence-1 VO (`S01`) | `10_Shorts/vo_v02/hos_008_short_C_s01_v03.wav` | `553,038` | `125c195fea535621610b39b4a314c0019946f0368c448d869401c1833712caac` |
| Sentence-1 STT JSON | `10_Shorts/vo_v02/stt/hos_008_short_C_s01_v03/stt_raw.json` | `2,009` | `04035abda689560edc732f7938a7d03c69926911fdbbc14c3e851f0decaa6eb3` |
| Body VO (`5.720–24.400 s`) | `10_Shorts/vo_v02/hos_008_short_C_v02.wav` | `4,700,238` | `0a25b6dab1351e70fad717d96e066f0d6c1981bd2d17eba1b65db719acec0aa0` |
| Body STT JSON | `10_Shorts/vo_v02/stt/hos_008_short_C_v02/stt_raw.json` | `17,177` | `feab2d929efd897f0804cd13eb321096f7bb50e7b1aa71bfb6814548fe84d70d` |
| Film score bed (`v02`) | `05_Music/lightning008_score_bed_v02.mp3` | `12,952,556` | `40937135976eeb99fe33acedc5924b0bd41f89b20244b81a2759da7792f4404c` |
| House SFX whoosh | `06_Sound-Effects/kit_v01/sfx_hos_whoosh_soft_v01.wav` | `192,044` | `6964b71eb719e32705d69cd08d6d7f5c637f804474153ec12295606e301958ed` |
| House SFX rumble | `06_Sound-Effects/kit_v01/sfx_hos_rumble_low_v01.wav` | `768,044` | `7c37a15593fd636137216b77c40a4311c8158b84d41770d547e7452437ce7571` |
| House SFX ink tick | `06_Sound-Effects/kit_v01/sfx_hos_tick_ink_v01.wav` | `11,564` | `98db8f2fa3b13009ea96249ab973c52cde133461c90945b34f0f0936d2127e9d` |
| Existing `v03` master (untouched) | `10_Shorts/hos_008_short_C_v03.mp4` | `16,055,783` | `9f25a16de5fc7d454be7adbc0e301614c7b060cd28b10cd076bcd2b4a6642161` |

---

## 4. Gates, Approvals & Elected-Chief Handoff Commands

- All original `J2485` / `J2662` constraints remain valid: zero-spend (`£0`) re-cut to `hos_008_short_C_v04.mp4` using existing voice and picture only, leaving `hos_008_short_C_v03.mp4` untouched, with no upload or schedule changes.
- Because `scripts/jobs.py` (`do_reopen`) enforces `chief_relay.elected_for(agent, at, job)` (`"Only the elected Chief may release a verified hold"`), `J2687` is parked for the elected Chief (`claude`) to run:

```bash
python3 scripts/jobs.py reopen J2662 --agent claude \
  --note "J2687 verified condition MET (jobs/reviews/J2687/REVIEW.md): all 8 HOS 008 Short C v03 raw source clips and the J2255 build recipe (_build_short_c_v03.py, sha256 0b59eb72...) are restored from Mini hos-008-lightning originals to both studio-live and the Mini shared HOS 008 folder with 3-way SHA-256 verification, and all VO/STT/music/SFX stems match across Mini and NAS. Ready to build and gate hos_008_short_C_v04.mp4 (£0)." \
  --git

python3 scripts/jobs.py done J2687 --agent claude \
  --result "Condition MET at 2026-11-13T08:51Z (jobs/reviews/J2687/REVIEW.md): restored all 8 HOS 008 Short C v03 raw source clips and J2255 _build_short_c_v03.py to studio-live and Mini shared HOS 008 folder with 3-way SHA-256 verification; reopened J2662 for £0 v04 re-cut." \
  --git
```
