# J2361 — OWB 034 Pluto Shot-List Repair (Addressing J2359 Chief FIX on PR #626)

- **Job:** `J2361` (`034 Pluto: repair shot-list source, reuse and finishing defects from J2359`)
- **Worker:** `gemini` (Gemini 4 Argon, specialist worker covering `J2361`; not Chief — no stage PASS, merge, or spend approval claimed)
- **Date:** 7 November 2026
- **Branch / PR:** `j2353-pluto-shot-list` (PR #626)
- **Spend:** **£0 / 0 credits** (zero-spend repair only; no generation, assembly, or upload performed).

---

## 1. Point-by-Point Repair of J2359 Blocking Findings

1. **DEM Reconstructions, Sphere-Rendered Flyovers & Annotated/Noisy Plates Replaced and Audited (`64` Clean Assets):**
   - Removed and banned `PIA21863` (DEM perspective reconstruction, formerly R06/R43), `PIA21864` (DEM perspective reconstruction, formerly R28 fallback), `File:Pluto-FlyoverAnimation-20150918.webm` (DEM flyover animation, formerly R38), `PIA19951` (sphere-rendered flyover animation frame), `PIA19965` (vertical-relief reconstruction), `PIA19873` (simulated flyby geometry), `PIA11709` (pre-flyby synthetic globe), and `PIA20589` (embedded red arrow + heavy sensor noise, formerly R64).
   - Audited every source against official NASA/Wikimedia descriptions and inspected every still at full resolution via `read_file`. Also rejected split-panel/callout/border-artifact plates (`PIA20464`, `PIA20361`, `PIA20151`, `PIA19690`, `PIA20200`, `PIA19937`, `PIA20213`, `PIA19955`, `PIA19945`, `PIA19943`, `PIA15546`, `PIA20212`, `PIA20641`, `PIA20581`, `PIA19706`, `File:Pits in Pluto's Sputnik Planum.jpg`).
   - Recorded exact canonical URLs, rights URLs, SHA-256 hashes, native/crop dimensions, 1080p upscale factors (`<= 1.58x`, well below the `2.35x` ceiling), and full-size visual audit notes for all `64` assets in `07_Edit-Project/SOURCE_EVIDENCE_v01.json` and §6 of `SHOT_LIST_v01.md`.
2. **Per-Cut Reuse Accounting & Canonical Exposure Deduplication (`<= 2` Raw and Separated Appearances Everywhere):**
   - Deduplicated underlying camera exposures: kept `PIA20291` (`R01`, `R46`) and banned `PIA19708` / `PIA19857` (same 13 July 2015 LORRI exposure); kept `PIA19932` (`R21`, `R22`) and banned `PIA19709`; kept `PIA19968` (`R24`, `R30`) and banned `File:Charon in True Color - High-Res.jpg`; kept `PIA19948` (`R63`, `R74`) and banned `PIA19947` (closer-look crop of `PIA19948`); kept `PIA01536` (`R73`) and banned `PIA02211`; kept `File:Reworked composite image of Arrokoth rotated.png` (`R68`, `R69`) and banned `File:UltimaThule CA06 color 20190516.png`.
   - Rebuilt per-row and separated appearance counts across all `74` rows including `CODE` graphic backgrounds/cutouts and `R30`/`R57` `[ORBIT ACTS]` zero-cost archive/overlay routes. Every single asset (`64` total) has **`<= 2` raw spoken/end-hold appearances** and **`<= 2` separated appearances** (fixing `PIA18033`, `PIA19948`, `PIA19966`, `PIA19936`, `PIA20198`, and `PIA21590`).
   - Explicitly distinguished the `5` native motion video assets from `animated still` pans/zooms and placed real moving spacecraft/observatory imagery between all `13` `CODE` rows (`0` adjacent `CODE` rows).
3. **Explicit `source=CARD` Chapter-Card Rows & Verified `0.60 s` Breaths (`clip_check.py` `74 rows — PASS`):**
   - Inserted `6` explicit `source=CARD` rows (`R08` `65.76–66.04 s`, `R20` `159.22–159.48 s`, `R33` `261.14–261.42 s`, `R45` `368.22–368.52 s`, `R54` `451.66–451.96 s`, `R64` `534.26–535.06 s`) into `shot_list_v01.csv`.
   - Every chapter card starts **exactly `0.60 s`** after the preceding spoken word finishes (`65.16 -> 65.76 s`, `158.62 -> 159.22 s`, `260.54 -> 261.14 s`, `367.62 -> 368.22 s`, `451.06 -> 451.66 s`, `533.66 -> 534.26 s`), with a `0.40 s` crossfade and zero clipped words (`clip_check.py` `74 rows — PASS`, `0` errors, `0` warnings).
4. **Repaired Music Ending & Verified `NOT:` List (`05_Music/MUSIC_BRIEF_v01.md` & `R74`):**
   - Updated `MUSIC_BRIEF_v01.md` and `R74` (`616.16–634.16 s`): `2.50 s` full-level post-word hold (`616.040–618.54 s`), nonzero bed throughout the `18.00 s` moving end hold, **`10.00 s` smooth music fade** over `624.16–634.16 s`, and **`2.00 s` final picture fade to black** over `632.16–634.16 s`.
   - Verified the `NOT:` line against the actual music briefs and film slugs in `003`–`033` (`013` Moon Leaving, `020` Jupiter, `021` Saturn Rings, `022` Sun Brighter, `023` Venus, `024` Light Speed, `025` Mars Robot, `026` Nearest Star, `027` Earth Stopped Spinning, `028` Gliese 710, `029` Betelgeuse, `030` Apophis, `031` Earth Magnetic Field, `032` Titan, `033` Uranus).
5. **Reconciled Counts, `<= 4`-Word Animated Labels, Measured Lifted Navy (`#162238`–`#1F3150`) & Frame-0 Evidence:**
   - Reconciled all counts across `shot_list_v01.csv`, `SHOT_LIST_v01.md`, `SOURCE_EVIDENCE_v01.json`, `SFX_PLAN_v01.md`, and `production-status.md`: `74` total rows (`67` spoken + `6` `CARD` + `1` End Hold), `13` `CODE` rows, `15` `WHEN` markers, `3` `WHO` cards, `4` `FACT` cards, `7` `DATA`/`SCALE`/`NUMBER OBJECT` sets, and `64` source-table assets.
   - Shortened all edit/overlay labels to **`<= 4` whitespace-delimited words** (e.g., `260 KM CRATERS`, `CONVECTING NITROGEN CELLS`, `MOONS UNDER 160 KM`, `58,536 KM/H LAUNCH SPEED`).
   - Replaced `#050814` (luma `~8`) with measured lifted starry navy `#162238`–`#1F3150` (`background_only_mean_luma = 40.22`, `p95_luma = 46.69`; `composed_r01_mean_luma = 57.20`, `p95_luma = 181.68`).
   - Recorded SHA-256 and crop/dimension proof that Frame 0 (`PIA20291`, `1024x1024`, SHA-256 `76065326978e0791…`) is distinct from standalone Short `gmzaCfJF1gA` Frame 0 (`PIA19952`, `5000x5000`, SHA-256 `257757c3f7a481a6…`).
6. **`R30` & `R57` (`[ORBIT ACTS #1]` & `[ORBIT ACTS #2]`, formerly `R28` & `R52`) Zero-Cost Archive/Overlay Route:**
   - Planned and typed `R30` (`235.56–249.04 s`, `PIA19968` Charon enhanced-colour globe with `153-HOUR` clock overlay and `FACT` #2 `CHARON NEVER SETS`) and `R57` (`473.52–482.12 s`, `PIA20198` al-Idrisi water-ice blocks -> `PIA19842` Hillary Montes with `2–3 KM WATER-ICE BLOCKS` label) as `source=NASA` zero-cost archive/overlay routes in `shot_list_v01.csv`. Bounded the footage search to `9` active minutes and `3` deep candidates (§5 of `SHOT_LIST_v01.md`).

---

## 2. Pasted `clip_check.py` Verification

```text
$ python3 00_Brand/Channel-Setup/tools/clip_check.py 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/shot_list_v01.csv --words 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_raw.json --vo-end 616.16
clip_check: 74 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.
```
