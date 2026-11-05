# J2173 — OWB `032` Titan Test A Opening Assessment & Exact Source-Time EDL (Reserve for Fri 27 Nov 2026)

- **Job:** `J2173` (`OWB locked-long Short: assess Titan Test A as reserve for 27 Nov`)
- **Parent Plan:** `J2023` (`jobs/reviews/J2023/PLAN.md`, `4e6927130d`)
- **Constrained Backlog / Audit Jobs:** `J0979` (`owb-short-from-locked`), `J1000` (`92a775ee8`), `J1042` (`3782768ab4`)
- **In-Progress Picture Dependency:** `J2089` (`032 picture: £0 harvest + code_graphics builds from SHOT_LIST_v02`, PR #491 `e0757a9ffe`, with `J2090` and `J2150` review rulings)
- **Reviewer / Worker:** `gemini` (`gemini-argon`)
- **Date:** 5 November 2026
- **Spend:** £0 (0 credits; no generation, no new VO, no speculative render, no upload/schedule/privacy/Buffer changes)
- **Capability Disclosure:** No `audio_input` or `moving_video_input` is claimed in this session (`chief_relay.py capabilities` recorded empty per `J1810` / 4 Nov rule; tool-provable hashes, Scribe word timings, and metadata verified; actual watching/listening is Ben's final watch).

---

## 1. Executive Verdict & Eligibility Summary

1. **Eligibility of `032` First `30–38 s` Opening as Test A:** **ELIGIBLE ON TEXT, TIMING & RULES (`s01`–`s05`, `0.060–31.580 s` master VO, 91 words) — HELD ON MISSING APPROVED PICTURE/MASTER INPUTS (`J2089` + `032` long master/score bed).**
   - Across `02_Voiceover/titan_landing_vo_v02b.wav` (`582.440 s`, 1,379 words, 80 sentences), the opening 5-sentence block **`s01`–`s05` (`0.060–31.580 s`, 91 spoken words)** is the **unique, self-contained sentence-end cut** inside the `30–38 s` Test A window (`05_Analytics/tests/SHORTS_TESTS.md`, `AGENTS.md` §5, `.cursor/rules/orbit-build-shorts.mdc`):
     - **Untrimmed 1:1 Master Timing (`32.800 s` total runtime):** `0.060–31.580 s` master VO (`31.520 s` spoken span, first word `"If"` at `0.100 s ≤ 0.15 s`, last word `"breathe."` at `31.520 s`) + `1.280 s` matched-cut loop tail (`≤ 1.50 s` ceiling) = **`32.800 s`** (`984` frames at `30 fps`), squarely inside the `30–38 s` Test A band (`< 40 s` hard cap).
     - **Breath-Tightened `<0.25 s` Seam Option (`30.000 s` total runtime):** Tightening the four inter-sentence breaths (`1.140 s`, `0.700 s`, `0.840 s`, `1.080 s`) to `0.200 s` each yields `28.560 s` spoken VO (`0.100–28.560 s`) + `1.440 s` loop tail = **`30.000 s`** (`900` frames at `30 fps`), satisfying both the `30–38 s` Test A floor and `LEARNINGS` rule 7 (`< 0.25 s` VO breath across the `4–5 s` sentence-1 seam).
   - **Why `s05` (`31.580 s`) is the only valid Test A sentence-end cut:**
     - `s03` (`22.500 s`, 65 words) and `s04` (`25.220 s`, 73 words) fall below the `30–38 s` Test A band and cut off before the lethal twist (`"What would kill you is the cold..."`).
     - `s06` (`32.759–35.900 s`: *"So why are the pebbles under your boots made of frozen water?"*) is an unanswered chapter-bridge question into Chapter 2.
     - `s07` (`38.900 s`), `s08` (`44.560 s`), and `s09` (`50.440 s`) exceed the `38.0 s` Test A band and/or the `40.0 s` Never-list hard cap.
   - **Keeper & `LEARNINGS` Rule 8 Compliance:** Even though Test A Shorts have an explicit exception from the `22–27 s` band and the one-question line-1 rule until Test A's readout in early January 2027 (`SHORTS_TESTS.md`), `032`'s opening **natively satisfies Keeper Rule 1 and `LEARNINGS` Rules 1, 2, 6, 8, and 10**:
     - Sentence 1 (`s01`, `0.160–5.240 s`) asks a positive Keeper-shape survival question naming both parent planet and moon: *"If you stepped out of a lander onto Saturn's largest moon, Titan, would you survive?"*
     - Zero meta-promise (`"In this film..."` was removed in `titan_landing_script_master_v02.md` / `titan_landing_vo_v02b`).
     - Payoff start (`s05`: *"What would kill you is the cold and the fact that there is almost no oxygen to breathe"*) lands at **`26.240 / 32.800 s = 80.0% ≥ 70%`** (`23.280 / 30.000 s = 77.6% ≥ 70%` in the tightened cut), passing `LEARNINGS` rule 6.
2. **Why `J0979` Cannot Be Reopened Today & Exact Missing Approved Inputs:**
   - Under `J2173` (*"Assess newly locked 032 first 30-38s opening as Test A ... after approved master exists; target 27Nov 11:30 only after planned 25Nov long public, final-watch pack by 20Nov 18:00. Source picture J2089 is still work in progress. Return exact EDL and eligibility; update/reopen J0979 only when its actual missing approved-input condition is satisfied, preserving progress; otherwise add exact dependency without generic retry"*):
   - **`J0979` is NOT reopened today** because four required £0 inputs do not yet exist:
     1. **Row 1 (`0.00–5.24 s`) Frame-0 Compliant Real Moving Subject (`J2089`):** `J2150` (`jobs/reviews/J2150/REVIEW.md`) excluded the ESA Huygens descent movie (`huygens_descent.wmv`, `sha256: 4b41648af46986687a907e6b960c564cb04740b157f22498bf8fab6532f21b97`) as a data-derived reconstruction (`picture_qa` FAIL). `J2089` (`1/4`, open) has not yet selected/harvested the replacement real moving subject plate for Row 1 / Frame 0.
     2. **Row 2 Mechanism (`survive_check`) & Row 3 Cassini Orbit Motion Clip (`J2089`):** Listed in `GRAPHICS_COVERAGE_v01.json` `remaining_builds` (`"R2 survive_check"`) and `J2089` remaining motion harvest; not yet rendered/selected. (Note: Row 3 `r03_pressure` and Row 4 `r04_cold` DATA overlays ARE rendered and verified on PR #491 `e0757a9ffe`, and `PIA14602.jpg` / `PIA08167.jpg` are downloaded.)
     3. **Film-Specific Score Bed (`05_Music/`):** `032` has no `05_Music/` directory or score bed yet (`music_gate.py` requires the film's own score bed).
     4. **Approved `032` Long Master & Chosen Listing Title (`07_Edit-Project/`, `11_Upload-Package/`):** Test A is reframed from the approved `032` long master (with its exact chosen listing title at `9.0–14.0 s` and YouTube ID for `relatedVideoId`), targeting **Fri 27 Nov 2026 11:30Z** (watch pack due **Fri 20 Nov 2026 18:00Z**) only after the planned **Wed 25 Nov 2026 18:00Z** `032` long is public (`J2023`, `J2147`).
   - **Queue Update Applied to `J0979`:** Preserved `J0979` `status: "blocked"` and `progress: 4/4`, updated `"after": "J2089"` and `"taskKeys": ["OWB:032"]`, and replaced the generic timed `"type": "input"` retry hold with an exact `"type": "dependency"` hold (no `check_at` polling loop) so `workflow_state.hold_due` fires only when `J2089` completes.

---

## 2. Exact Media, Source & Hash Inventory (`OWB:032` & Existing Shorts)

### 2.1 Verified `032` Repo & Cache Files (5 Nov 2026)

| Asset / File | Path | Size (Bytes) | SHA-256 | Status |
|---|---|---:|---|---|
| Locked Script v02 | `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/01_Script/titan_landing_script_master_v02.md` | `19,269` | `debeecc351988053cb3af56e8e0844b5ebf79251871cf9a9929456a7d8b4106e` | **LOCKED** (29 Oct; agenda line removed per `LEARNINGS` rule 10) |
| Sources Table | `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/01_Script/SOURCES.md` | `65,692` | `3174255d2b390b8669d69f33b3e555b86e7526f4a4895824cdda723d3c51c0f3` | **PASS** (`J0301` `97b7af4ee9`, reconciled in `J1773`) |
| Sources Reconciliation | `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/01_Script/J1773_SOURCES_RECONCILIATION.md` | `2,148` | `8c05b449ebb8e3c946b9402003beda531e227cc526caf3a2133967429e6c7726` | **PASS** (`J1773`) |
| Locked VO WAV (`v02b`) | `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/02_Voiceover/titan_landing_vo_v02b.wav` | `111,828,558` | `55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5` | **LOCKED** (`582.440 s`, `-20.0 LUFS`, `-3.4 dBFS TP`; `J1294` / `J1753`) |
| Locked VO MP3 (`v02b`) | `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/02_Voiceover/titan_landing_vo_v02b.mp3` | `9,320,108` | `944378a9c7caec4368217a481d35160cfb5621ed4de7dbe4a7787d813a6abff8` | **LOCKED** (`J1294` / `J1753`) |
| Scribe Word Timings | `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/02_Voiceover/stt/titan_landing_vo_v02b/stt_raw.json` | `395,987` | `dfdc6b91186ade0a92b8389b6755241ff07dab147b8050d8b2937d8463b12a8a` | **VERIFIED** (1,379 words, 80 sentences) |
| Word SRT | `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/02_Voiceover/stt/titan_landing_vo_v02b/words.srt` | `15,085` | `63385f68b5a6f0c78ed347bc44778cbdd1e92b0cc0f2c5428965e647e3865335` | **VERIFIED** |
| Shot List v02 (`main`) | `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/SHOT_LIST_v02.md` | `25,580` | `a2ac9ed41e4094645440706f8f803f2e28f91be47878a4abec5710a297534dc1` | **Rule-E GO** (`J2044` `7b45d14ba1`) |
| Shot List v04 (`PR #491`) | `07_Edit-Project/SHOT_LIST_v04.md` (`e0757a9ffe`) | — | `b600d2bc92414d9eb80c92d4554460df9ac68934150cf4426e87a1da0e097d81` (v03 base) | **WIP (`J2089` 1/4)** (`J2090` + `J2150` applied) |
| Row 3 Still (`PIA14602`) | `/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA14602.jpg` | `29,547` | `3e893445ca67c27e51975eec92f943d43f7bf79ca65a1659f315d390cb20faed` | **DOWNLOADED** (`J2090` replacement for `PIA14909`, 1024×1024) |
| Row 4 Still (`PIA08167`) | `/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA08167.jpg` | `43,289` | `66df7c709f04c2fda66d290d0130ac23b53b9d1895fabcd4f9689913745a4a83` | **DOWNLOADED** (`J2090` replacement for `PIA08399`, 923×603) |
| Row 3 DATA Render (`r03_pressure`) | `/Users/benjaminoats/_desk/cache/J2089/data_renders_v02/code_graphic_032_r03_pressure_v01.mov` | — | `ff29d48de28942c81c4dd1bfbec0244c63c601144e0b6449dcb445bc1249fdf0` | **RENDERED** (`J2150` KEEP; `1 bar` vs `1.47 bar`, 3.6 s ARGB) |
| Row 4 DATA Render (`r04_cold`) | `/Users/benjaminoats/_desk/cache/J2089/data_renders_v02/code_graphic_032_r04_cold_v01.mov` | — | `229f830338dac3a12ba762a407fb516923ac81a4ad6e0d670b7c5a12a45e996a` | **RENDERED** (`J2150` CHANGE applied: `TITAN SURFACE` `-179 °C` + `ALMOST NO OXYGEN` footnote) |
| Excluded Descent Movie | `/Users/benjaminoats/_desk/cache/J2089/additional_v01/huygens_descent.wmv` | `155,564,728` | `4b41648af46986687a907e6b960c564cb04740b157f22498bf8fab6532f21b97` | **EXCLUDED (`J2150`)** — data-derived reconstruction (`picture_qa` FAIL) |

### 2.2 Duplicate Idea, Schedule & Asset Check (`2026-11-04.json` Snapshot + `UPLOADS.json`)

1. **Existing Titan Standalone Short (`RLSJm59OSzI`, scheduled Tue 10 Nov 2026 11:30Z):**
   - **Title:** *"What Would Standing on Saturn's Moon Titan Feel Like?"* (`owb_sa_s6_titan_v02.mp4`, `18.0 s`, `sha256: be16daeb17284ea3d20148a1e6f8e3ea7ab6cdec64cf22e47f92b6167780b97d`).
   - **Spoken Script (36 words):** *"Standing on Titan feels like being 15 meters underwater. The air on Saturn's biggest moon presses 60% harder than ours, so NASA is sending Dragonfly, a flying robot. It launches in 2028 and lands in 2034."*
   - **Comparison with `032` Test A (`s01`–`s05`, 91 words):**
     - `RLSJm59OSzI` is an unlinked `J0216` standalone test Short airing 17 days earlier (10 Nov vs 27 Nov) that focuses on the `15 m` underwater analogy and the `2028`/`2034` Dragonfly launch/landing dates.
     - `032` Test A (`s01`–`s05`) asks the survival question (*"If you stepped out of a lander onto Saturn's largest moon, Titan, would you survive?"*), busts the vacuum explosion/boiling-blood myth (`1.47 bar ≈ 1.5× Earth` pressure won't hurt you), and lands on the lethal twin killers: **`−179 °C` deep freeze and almost zero oxygen to breathe**.
     - **Zero Frame / Asset Overlap:** `RLSJm59OSzI` uses `PIA14925`, `PIA06230`, `PIA09739`, and `PIA21625`. All four are explicitly barred from `032` (`HARVEST_POOL_v01.json` `excluded_short_asset_ids` and `J2090`).
2. **24–29 November 2026 OWB Schedule Window (`J2023/PLAN.md`):**
   - **Sun 22 Nov 18:00Z:** `027` Long `6bbbvfCx6zY` (*What If Earth Stopped Spinning?*).
   - **Mon 23 Nov 11:30Z:** `027` Short `emwQsPxnRGM` (*Why Do You Weigh Less at Earth's Equator?*).
   - **Wed 25 Nov 11:30Z (Provisional):** `AR2` (*ISS deorbit*, `J1471` → `J1356`, watch pack due 20 Nov 18:00Z).
   - **Wed 25 Nov 18:00Z (Planned):** `032` Long (*What Would Happen If You Landed on Titan?*, new Wednesday long slot per `J2147` / Ben 4 Nov order).
   - **Fri 27 Nov 11:30Z (Provisional Target):** `AR1` (*2024 YR4 Moon miss*) **OR** `032` Titan Test A as replacement reserve (**never both on the same day**; `032` long must be public on Wed 25 Nov 18:00Z before `032` Test A airs on Fri 27 Nov 11:30Z; final-watch pack due **Fri 20 Nov 2026 18:00Z**).
   - **Sat 28 Nov 11:30Z (Provisional):** `AR3` (*2027 eclipse*).
   - **Sun 29 Nov 18:00Z:** `028` Long `F-jImX5h7ws` (*What Happens When a Star Passes Through Our Solar System?*).
   - **Short Count Cap for `032`:** Under `AGENTS.md` ("Two OWB longs a week": *"Each new OWB long gets **two** Shorts (one is Test A's opening Short while that test runs)"*) and `J2173` (*"No extra Test A or third new Short for 032"*), `032` gets at most **two** new Shorts total (one being this Test A opening Short, and at most one dedicated/lifted second Short planned under `J2147`).

---

## 3. Sentence-by-Sentence Audit of `032` Chapter 0 Opening (`0.160–50.440 s`)

From `02_Voiceover/stt/titan_landing_vo_v02b/stt_raw.json` (`sha256: dfdc6b91186ade0a92b8389b6755241ff07dab147b8050d8b2937d8463b12a8a`):

| Sent # | Master Span (s) | Dur (s) | Gap After (s) | Words | Cum. Words | Verbatim Spoken Text | Cut-Point Verdict for Test A (`30–38 s` Window) |
|---|---|---:|---:|---:|---:|---|---|
| `s01` | `0.160–5.240` | `5.080` | `1.140` | 15 | 15 | *"If you stepped out of a lander onto Saturn's largest moon, Titan, would you survive?"* | Opening hook question (`< 30 s`). Names `"Saturn's largest moon, Titan"` (`2.000–3.860 s`). |
| `s02` | `6.380–9.360` | `2.980` | `0.700` | 11 | 26 | *"Your body would not explode, and your blood would not boil."* | Immediate myth-bust (`< 30 s`). |
| `s03` | `10.060–22.500` | `12.440` | `0.840` | 39 | 65 | *"In fact, while spacecraft in orbit around Saturn fly through a vacuum, Titan wraps itself in an orange nitrogen sky that presses on you about one and a half times harder than the air in your room right now."* | Concrete number (`1.5×` / `1.47 bar` vs `1 bar`, `SOURCES.md` row 1), but `22.500 s` is `< 30 s` Test A floor and incomplete without the survival twist. |
| `s04` | `23.340–25.220` | `1.880` | `1.080` | 8 | 73 | *"That pressure would not hurt you at all."* | Setup for lethal contrast (`25.220 s < 30 s`). |
| **`s05`** | **`26.300–31.580`** | **`5.280`** | **`1.179`** | **18** | **91** | ***"What would kill you is the cold and the fact that there is almost no oxygen to breathe."*** | **ELIGIBLE TEST A CUT POINT (`31.580 s` VO end → `32.800 s` with `1.280 s` loop tail, or `30.000 s` breath-tightened).** Complete answer + payoff (`80.0%` runtime start). |
| `s06` | `32.759–35.900` | `3.141` | `0.700` | 12 | 103 | *"So why are the pebbles under your boots made of frozen water?"* | **INELIGIBLE:** Unanswered chapter-bridge question into Ch 2. |
| `s07` | `36.600–38.900` | `2.300` | `0.540` | 8 | 111 | *"Why does its rain fall in slow motion?"* | **INELIGIBLE:** Ends at `38.900 s > 38.0 s` Test A band (`> 40.0 s` with loop tail); unanswered bridge question. |
| `s08` | `39.440–44.560` | `5.120` | `1.060` | 17 | 128 | *"And why is this mysterious world so good for flying that NASA is sending a drone there?"* | **INELIGIBLE:** `44.560 s > 40.0 s` Never-list hard cap. |
| `s09` | `45.620–50.440` | `4.820` | `0.820` | 19 | 147 | *"Why did it take so long to discover that a moon could hold onto a sky of its own?"* | **INELIGIBLE:** `50.440 s > 40.0 s` Never-list hard cap. |

---

## 4. Exact Source-Time EDL for `032` Test A (`s01`–`s05`, 91 Words)

### 4.1 Proposed Packaging & Overlay Spec

- **Short Title (Keeper Rule 1 positive question matching `s01`):**
  - Primary: **`Could You Survive Stepping Onto Saturn's Moon Titan?`** (51 chars; matches `s01` *"If you stepped out of a lander onto Saturn's largest moon, Titan, would you survive?"*, distinct from long draft title *"What Would Happen If You Landed on Titan?"* and from standalone `RLSJm59OSzI` *"What Would Standing on Saturn's Moon Titan Feel Like?"*).
- **Frame-0 Hook Caption (`0.00–2.20 s`):** **`STEP OUT / ON TITAN?`** (yellow hook word: `TITAN?`, 2 lines, 4 words, inside 16:9 safe band, clear of subject).
- **Mid-Short Promo Title Banner (`9.00–14.00 s`):** Exact chosen listing title of `032` long (provisional: **`What Would Happen / If You Landed / on Titan?`**; must be verified against the final approved `032` upload manifest before assembly).
- **Single Teach Overlay (`AGENTS.md` *Teach on screen* — at most 1 overlay in a Short, clear of `0–2 s` and `9–14 s`, inside 16:9 centre band):**
  - **`1.47 BAR (1.5× EARTH)`** (`r03_pressure` native 9:16 reframe / bar at `18.20–21.80 s` in Table A, or `16.46–20.06 s` in Table B, while VO says *"presses on you about one and a half times harder than the air in your room right now"*).
  - Note: During `s05` (`26.24–31.52 s`), `r04_cold` (`-179 °C` / `TITAN SURFACE`) runs as the underlying visual plate graphic, or if `r03_pressure` is counted as the single teach overlay, `s05` uses the graded real Cassini stratospheric haze plate (`PIA08167` / `PIA21902`) so the Short carries strictly **one** teach graphic/overlay (`AGENTS.md`: *"Shorts: at most one overlay"*).

### 4.2 Table A — 1:1 Master-Timed EDL (`32.800 s` Total Runtime; `-60 ms` Start Pad Trim Only)

 trims `0.000–0.060 s` leading silence from `titan_landing_vo_v02b.wav` (`timeline_t = master_t - 0.060 s`) so word 1 (`"If"`) starts at **`0.100 s ≤ 0.150 s`**, preserving 100% of the long master's internal pacing from `0.060 s` to `31.580 s` (`31.520 s` VO + `1.280 s` loop tail = **`32.800 s`**, `984` frames at `30 fps`):

| Cut # | Timeline In–Out (s) | Dur (s) | Master VO Span (s) | Spoken Words in Cut | `SHOT_LIST_v04` / `J2089` Source Asset | Current Input Status (`J2089` PR #491) |
|---:|---|---:|---|---|---|---|
| `c01` | `0.00–2.64` | `2.64` | `0.060–2.700` | *"If you stepped out of a lander onto Saturn's largest"* (w1–10) | **Row 1 Open (part A):** Real moving Titan subject footage (≥60% fill, ≤30% black, no Orbit, hook caption `STEP OUT / ON TITAN?` `0.0–2.2 s`, rumble SFX at `0.0 s`) | **MISSING (`J2089`):** `J2150` excluded `huygens_descent.wmv` reconstruction; `J2089` must supply compliant real moving subject plate |
| `c02` | `2.64–5.80` | `3.16` | `2.700–5.860` | *"moon, Titan, would you survive?"* (w11–15; `s01` ends `5.180 s` timeline) | **Row 1 Open (part B):** Reframed/second angle of real moving Titan approach/limb footage bridging `s01` end | **MISSING (`J2089`):** Depends on Row 1 real moving footage selection |
| `c03` | `5.80–9.30` | `3.50` | `5.860–9.360` | *"Your body would not explode, and your blood would not boil."* (w16–26; `s02` `6.320–9.300 s`) | **Row 2 (`survive_check`):** Graded amber Titan haze plate with animated check graphic (`WON'T EXPLODE ✓`, `BLOOD WON'T BOIL ✓`) | **MISSING (`J2089`):** `R2 survive_check` listed in `GRAPHICS_COVERAGE_v01.json` `remaining_builds` |
| `c04` | `9.30–13.10` | `3.80` | `9.360–13.160` | *"In fact, while spacecraft in orbit around Saturn"* (w27–34) | **Row 3 (part A):** Cassini in orbit around Saturn (JPL mission animation, 9:16 centre crop) + `9.0–14.0 s` exact long title banner | **WIP (`J2089`):** JPL Cassini orbit animation harvest/interval selection pending in `J2089` |
| `c05` | `13.10–16.80` | `3.70` | `13.160–16.860` | *"fly through a vacuum, Titan wraps itself in an orange"* (w35–44) | **Row 3 (part B):** Cassini natural-colour orange Titan (`PIA14602.jpg`, `sha256: 3e893445...`, dynamic 9:16 pan/push, completes `9.0–14.0 s` title banner) | **DOWNLOADED (`J2089`):** `PIA14602.jpg` verified via `J2090` |
| `c06` | `16.80–20.20` | `3.40` | `16.860–20.260` | *"nitrogen sky that presses on you about one and a half times"* (w45–56) | **Row 3 (part C, Single Teach Graphic):** `code_graphic_032_r03_pressure_v01.mov` (`sha256: ff29d48d...`, `EARTH 1 BAR` vs `TITAN 1.47 BAR`) composited over graded moving Titan plate + ink tick at `17.10 s` | **RENDERED (`J2089`/`J2150`):** `r03_pressure` MOV verified; composite over graded plate pending `J2089` |
| `c07` | `20.20–23.20` | `3.00` | `20.260–23.260` | *"harder than the air in your room right now."* (w57–65; `s03` ends `22.440 s`) | **Row 4 (part A):** Cassini northern haze layers (`PIA08167.jpg`, `sha256: 66df7c70...`, wide 9:16 push) | **DOWNLOADED (`J2089`):** `PIA08167.jpg` verified via `J2090` |
| `c08` | `23.20–26.18` | `2.98` | `23.260–26.240` | *"That pressure would not hurt you at all."* (w66–73; `s04` `23.280–25.160 s`) | **Row 4 (part B):** Cassini detached twilight haze layers (`PIA21902.jpg` from R11 pool, distinct plate so `PIA08167` is not held >4 s) | **DOWNLOADED (`J2089`):** `PIA21902.jpg` verified via `J2090` |
| `c09` | `26.18–29.20` | `3.02` | `26.240–29.260` | *"What would kill you is the cold and the fact"* (w74–83; **Payoff starts `26.240 s = 80.0%`**) | **Row 20 / Row 18 Surface Ice Payoff (`PIA07232.jpg`):** Huygens DISR surface water-ice pebbles in amber light (inset/crop per `J2090` `≤2.0×` upscale rule over graded plate) | **DOWNLOADED (`J2089`):** `PIA07232.jpg` crop/composite pending `J2089` |
| `c10` | `29.20–31.52` | `2.32` | `29.260–31.580` | *"that there is almost no oxygen to breathe."* (w84–91; `s05` ends `31.520 s`) | **Row 6 (`PIA14922.jpg`):** Cassini natural-colour orange Titan before ringed Saturn (`sha256: 4513d54d...`, 1417×1326, 9:16 push) | **DOWNLOADED (`J2089`):** `PIA14922.jpg` verified via `J2090` |
| `c11` | `31.52–32.80` | `1.28` | *(loop tail)* | *(Music + moving picture only; `1.280 s ≤ 1.50 s` ceiling)* | **Loop Tail to Frame 0:** Last `1.28 s` preroll of Row 1 opening moving clip so frame `984` matches frame `0` (`loop_diff < 2.0`), no end card in last 2 s | **MISSING (`J2089`):** Depends on Row 1 opening moving clip |

### 4.3 Table B — Breath-Tightened `<0.25 s` Seam EDL (`30.000 s` Total Runtime)

If the assembler tightens the four inter-sentence pauses to `0.200 s` each (per `.cursor/rules/orbit-build-shorts.mdc` & `LEARNINGS` rule 7: keep sentence breaths `< 0.25 s`):

| Sent # | Master VO Span (s) | Master Dur (s) | Timeline VO Span (s) | Breath After (s) | Words | Notes |
|---|---|---:|---|---:|---:|---|
| `s01` | `0.160–5.240` | `5.080` | `0.100–5.180` | `0.200` (was `1.140`) | 15 | First word `"If"` at `0.100 s`; `"Saturn's"` at `1.940 s`; `"Titan"` at `3.320 s`; `"survive?"` ends `5.180 s`. Cut 1 at `2.64 s`, Cut 2 at `5.28 s`. |
| `s02` | `6.380–9.360` | `2.980` | `5.380–8.360` | `0.200` (was `0.700`) | 11 | Bridges `5.18–5.38 s` seam (`0.20 s < 0.25 s`) directly into *"Your body would not explode..."*. Cut 3 at `8.46 s`. |
| `s03` | `10.060–22.500` | `12.440` | `8.560–21.000` | `0.200` (was `0.840`) | 39 | Runs across `9.0–14.0 s` exact long title banner (`c04` `8.46–12.00 s`, `c05` `12.00–15.60 s`) and `r03_pressure` single teach graphic (`c06` `15.60–19.20 s`, `c07` `19.20–21.10 s`). |
| `s04` | `23.340–25.220` | `1.880` | `21.200–23.080` | `0.200` (was `1.080`) | 8 | *"That pressure would not hurt you at all."* (`c08` `21.10–23.18 s`). |
| `s05` | `26.300–31.580` | `5.280` | `23.280–28.560` | `1.440` (loop tail) | 18 | **Payoff starts `23.280 / 30.000 s = 77.6% ≥ 70%` PASS.** Ends `28.560 s`; `1.440 s` loop tail (`28.560–30.000 s`, `≤ 1.50 s`) completes `30.000 s` (`900` frames). |

### 4.4 Learnings & Brief Checklist Verification for `032` Test A (`s01`–`s05`)

- **#1 · Title:** Positive question in Keeper survival shape: *"Could You Survive Stepping Onto Saturn's Moon Titan?"* (asked directly in `s01`).
- **#2 · Frame 0 + spoken subject in `0–2.5 s`:** Spoken `s01` names `"Saturn's"` at `2.000–2.460 s` (`1.940–2.400 s` trimmed, `≤ 2.5 s`), `"moon"` at `2.980 s`, and `"Titan"` at `3.380 s`, with `STEP OUT / ON TITAN?` on frame 0 (`0.0–2.2 s`). Frame 0 visual requires `J2089`'s replacement real moving Titan clip (≥60% fill, ≤30% black, `visor_frac = 0.0`).
- **#3 · Motion (no static zoom in `4–8 s`, max hold `≤ 4.0 s`):** 11 cuts across `32.80 s` (`2.32–3.80 s` per cut; longest hold `3.80 s ≤ 4.0 s`). Beat times (Table A): `0.00 s`, `2.64 s`, `5.80 s`, `9.30 s`, `13.10 s`, `16.80 s`, `20.20 s`, `23.20 s`, `26.18 s`, `29.20 s`, `31.52 s`.
- **#6 · Payoff (`≥ 70%` of runtime):**
  - Table A (`32.80 s`): earliest allowed payoff (`0.70 × 32.80`) = `22.96 s`; actual lethal payoff (`s05`: *"What would kill you is the cold and the fact that there is almost no oxygen to breathe"*) starts at **`26.24 s` (`80.0% ≥ 70%` PASS)**.
  - Table B (`30.00 s`): earliest allowed payoff (`0.70 × 30.00`) = `21.00 s`; actual lethal payoff starts at **`23.28 s` (`77.6% ≥ 70%` PASS)**.
  - Neither cut resolves the question during the `9.0–14.0 s` promo banner.
- **#7 · Seam (`4–5 s` sentence-1 boundary):** Cut 1 lands at `2.64 s` (`≤ 3.0 s`) and Cut 2/3 bridges `s01` → `s02` (`"Your body would not explode, and your blood would not boil"`) with zero Orbit reaction and zero meta-promise. (Table B tightens the `s01`→`s02` breath from `1.14 s` to `0.20 s < 0.25 s`.)
- **#8 · 60% stayed-to-watch brief fields:**
  - Frame-0 source: Row 1 real moving Titan plate (pending `J2089` after `J2150` exclusion of `huygens_descent.wmv`)
  - First-word onset: `0.100 s ≤ 0.15 s` (`"If"`)
  - Surprise / stakes claim: `"stepped out of a lander onto Saturn's largest moon, Titan, would you survive?"` + hook caption `STEP OUT / ON TITAN?` at `0.00 s`
  - First cut: `2.64 s ≤ 3.0 s`
  - Meta-promise present: `no` (agenda sentence removed in `v02`)
  - Gap from last word to loop: `1.28 s ≤ 1.50 s` (Table A) / `1.44 s ≤ 1.50 s` (Table B)
- **#9 · 70% average viewed brief fields:**
  - Runtime: `32.80 s` (Table A) / `30.00 s` (Table B) — Test A `30–38 s` window (`SHORTS_TESTS.md`)
  - Longest plate hold: `3.80 s ≤ 4.0 s`
  - Payoff start vs `0.70 × runtime`: `26.24 s ≥ 22.96 s` (`80.0%`, Table A) / `23.28 s ≥ 21.00 s` (`77.6%`, Table B)
  - Loop sentence (`s05` → `s01`): *"What would kill you is the cold and the fact that there is almost no oxygen to breathe — if you stepped out of a lander onto Saturn's largest moon, Titan, would you survive?"* (reads continuously as one conditional sentence across the loop seam).

---

## 5. Complete Question-by-Question Audit of `032` Locked VO (`titan_landing_vo_v02b`)

For completeness under `J0979` / `J1000`, all 15 questions across the 80 sentences of `032` (`0.160–582.380 s`) were checked:

| Sent # | Master Span (s) | Dur (s) | Verbatim Spoken Question | Names `"Titan"` in Sent 1 (`0–2.5 s`)? | Verdict |
|---|---|---:|---|---|---|
| `s01` | `0.16–5.24` | `5.08` | *"If you stepped out of a lander onto Saturn's largest moon, Titan, would you survive?"* | Yes (`"Saturn's"` `2.00 s`, `"Titan"` `3.38 s`) | **ELIGIBLE AS TEST A (`s01`–`s05`, `0.06–31.58 s`, §3–§4 above).** |
| `s06` | `32.76–35.90` | `3.14` | *"So why are the pebbles under your boots made of frozen water?"* | No | **Ineligible:** Anaphoric `"So why..."`; unanswered chapter bridge. |
| `s07` | `36.60–38.90` | `2.30` | *"Why does its rain fall in slow motion?"* | No (pronoun *"its"*) | **Ineligible:** Anaphoric pronoun *"its"*; unanswered bridge. |
| `s08` | `39.44–44.56` | `5.12` | *"And why is this mysterious world so good for flying that NASA is sending a drone there?"* | No (*"this mysterious world"*) | **Ineligible:** Anaphoric; unanswered bridge. |
| `s09` | `45.62–50.44` | `4.82` | *"Why did it take so long to discover that a moon could hold onto a sky of its own?"* | No (*"a moon"*) | **Ineligible:** Omits `"Titan"`; leads into 86 s Ch 1 chronology (`1655`–`1980`). |
| `s17` | `126.02–133.60` | `7.58` | *"Why does Titan still have methane in its sky when sunlight keeps breaking it apart and should have used it up long ago?"* | Yes (`126.54–126.96 s`) | **Ineligible:** Unanswered bridge question at end of Ch 1 (followed by `s18` and Ch 2's 2005 Huygens landing, which does not answer the methane reservoir question). |
| `s18` | `134.40–136.68` | `2.28` | *"And what was hiding beneath the clouds?"* | No | **Ineligible:** Anaphoric conjunction + omits `"Titan"`. |
| `s27` | `202.52–205.82` | `3.30` | *"So why were the pebbles rounded as if by running liquid?"* | No | **Ineligible:** Anaphoric (*"the pebbles"*); omits `"Titan"` (`"Titan"` not spoken in `s27`–`s30`). |
| `s31` | `233.96–239.50` | `5.54` | *"Yet if you stepped out beside it in a heated suit, what would you feel when the rain began to fall?"* | No (pronoun *"it"*) | **Ineligible:** Anaphoric pronoun *"it"* (refers to Huygens probe) + sits immediately before `[SUBSCRIBE BEAT]`. |
| `s39` | `288.12–290.40` | `2.28` | *"What would you see if a storm rolled overhead?"* | No | **Ineligible:** Omits `"Titan"` in sentence 1 (`"Titan"` not spoken until `s41` at `298.94 s`, `10.82 s` later). |
| `s44` | `321.18–322.00` | `0.82` | *"Case closed?"* | No | **Ineligible:** 2-word fragment. |
| `s45` | `322.66–324.44` | `1.78` | *"Is Titan just a dry desert?"* | Yes (`322.94–323.40 s`, `0.28–0.74 s` into sentence) | **Note (Secondary Ch 4 Lift Candidate `s45`–`s48`, `322.66–354.22 s`):** Names `"Titan"` at `0.28 s` and answers with Cassini's north-pole radar discovery of Kraken Mare (`400,000 km² ≈ 5× Lake Superior`). However, `J2173` explicitly directs: *"Assess newly locked 032 first 30-38s opening as Test A... No extra Test A or third new Short for 032."* |
| `s55` | `389.76–396.76` | `7.00` | *"What if a spacecraft landed near those seas of liquid natural gas and fired its hot thrusters or struck a spark?"* | No (*"those seas"*) | **Ineligible:** Anaphoric demonstrative *"those seas"*; omits `"Titan"` in sentence 1. |
| `s57` | `402.02–411.64` | `9.62` | *"With hundreds of times more liquid hydrocarbons than all the known oil and natural gas reserves on Earth, wouldn't a single spark blow the lander apart?"* | No | **Ineligible:** Omits `"Titan"` in sentence 1 (`9.62 s` setup clause). |
| `s68` | `464.44–474.10` | `9.66` | *"So if Titan will not explode, and its thick nitrogen blanket cushions anything moving through it, how will humanity explore this strange world next?"* | Starts `"So if Titan..."` (`465.00 s`) | **Ineligible:** Anaphoric chapter-bridge transition (`9.66 s` question) into Ch 6 Dragonfly (`2028`/`2034`), which also overlaps `RLSJm59OSzI`'s Dragonfly `2028`/`2034` beat. |

---

## 6. Queue Disposition & Next Steps (`J0979` & `J2173`)

1. **`J0979` (`owb-short-from-locked`):**
   - Kept **`blocked`** with its `4/4` progress preserved (`029` `lift_die_young_10my` `v01` remains permanently shelved under `J1042`).
   - Updated `"after": "J2089"` and `"taskKeys": ["OWB:032"]`.
   - Replaced the generic timed `"type": "input"` hold with a structured `"type": "dependency"` hold (no `check_at` polling loop) naming the exact missing approved inputs:
     1. Completion of `J2089` (`032` £0 picture harvest + remaining graphics, specifically Row 1 Frame-0 compliant real moving subject after `J2150` exclusion of `huygens_descent.wmv`, Row 2 `survive_check`, and Row 3 Cassini orbit clip);
     2. `032` film-specific score bed (`05_Music/`) and approved `032` long master (`07_Edit-Project/`);
     3. Final chosen `032` long listing title and YouTube video ID (`11_Upload-Package/`, planned **Wed 25 Nov 2026 18:00Z** go-public before **Fri 27 Nov 2026 11:30Z** Test A slot, with final-watch pack due **Fri 20 Nov 2026 18:00Z**, replacing `AR1` only if approved and never running as a second Short on 27 Nov).
2. **`J2173`:** Closed `done` with this commit and report reference.
