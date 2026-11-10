# Packaging Panel Decision — OWB 026 (`How Far Is the Nearest Star?` / J1823 `abc_v04` Distance-Hook Candidates)

- **Date:** 2026-11-04
- **Job:** J1943 (`gemini`, Gemini 4 Argon; advisory packaging panel synthesis — the Elected Chief's exact-file ruling stands via `J1944`)
- **Evidence reviewed:** Commit `cecd5dc02c` (`jobs/reviews/J1823_v04.md`, `jobs/reviews/J1924.md`, `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/08_Thumbnail/abc_v04/META.json`, `nearest_star_thumb_B_v04.jpg`, `nearest_star_thumb_C_v04.jpg`, `comparison_true_168x94.png`, `GATE.txt`), `01_Script/nearest_star_script_master_v01.md`, `11_Upload-Package/PACKAGE_MANIFEST.json`, `11_Upload-Package/Descriptions/nearest_star_long_description_v01.txt`, and `11_Upload-Package/Captions/nearest_star_long_v06_en-GB.srt`.
- **Exact-file SHA-256 verification:** All 5 `abc_v04` artifact hashes (`nearest_star_thumb_B_v04.jpg`: `93f6e2a039e7c761503a26c8b550fcd156849adc31dfd18c65856ae96e61be4c`, `nearest_star_thumb_C_v04.jpg`: `40eccaf47c5ad885cb964218825e3ca23892e76c82463c83d2b863b5ca68148f`, `comparison_true_168x94.png`: `312acfa03fc473d61c5c73a82c3dd41bee82c17d8f8b468dcaac33a6c01616a2`, `tool_preview.jpg`: `80ebed33c22b3f497d704df273be88c2bcbaef8f2e5fe30e48de4076f9ad7bb1`, `GATE.txt`: `a34c132a65c9efe2f0143721328ada42c984eb480068d0f705dc4207775c4170`) and all 17 preserved `abc_v01/v02/v03` hashes (including Original Variant A `922855804c4a846fc82f1269d0e524b5b89bde781c187afe5f416367aa970216`) match `META.json`.
- **Critiques weighed:** `codex.md` (J1940), `gemini.md` (J1941), `cursor.md` (J1942, covered by Gemini Argon while Cursor was out of usage; note per `J1924` that `gemini.md` and `cursor.md` are independent runs by the same model family alongside `codex.md`).
- **Rule applied:** Where two or more critics agree (`< 8/10`), act on it; where two or more score `≥ 8/10`, keep. Review only — no live YouTube, Studio, manifest, or `THUMB_LEDGER.json` changes are made by this job.

---

## Summary Table

| Item | `codex.md` (J1940) | `gemini.md` (J1941) | `cursor.md` (J1942) | Panel Consensus |
|---|---:|---:|---:|---|
| **1. Title:** `How Far Is the Nearest Star?` | 8/10 | 8/10 | 8/10 | **KEEP** (3 of 3 score `8/10`; locked per brief) |
| **2. Thumbnail at `168×94`** (`B v04` / `C v04` vs `A`) | B: 7/10 · C: 7/10 | B: 7/10 · C: 5/10 (A: 7.5) | B: 6.5/10 · C: 5.5/10 (A: 8) | **KEEP Original A (`YOU CAN'T SEE IT`); select `B v04` (`900M YEAR WALK`) over `C v04` (`4.2 LIGHT YEARS`), with layout option for `J1944` on the Earth cutout** |
| **3. Title + Thumbnail Pair** | +B: 9/10 · +C: 6/10 | +B: 8/10 · +C: 4/10 (+A: 8.5) | +B: 7.5/10 · +C: 4.5/10 (+A: 8.5) | **KEEP Title + A & Title + `B v04` (`900M YEAR WALK`, 2 of 3 score `≥ 8/10`); REJECT `C v04` (`4.2 LIGHT YEARS`, 3 of 3 score `< 8/10`)** |
| **4. First 30 Seconds / Short Hook** | 7/10 | 7.5/10 | 8/10 | **KEEP** (locked `v06` VO/cut; note `0:20.8–0:33.1` agenda sentence for future scripts only) |
| **5a. Description First Paragraph** | 8/10 (keep) | 8.5/10 (keep) | 7.5/10 | **KEEP** (2 of 3 vote to keep first paragraph unchanged) |
| **5b. Description Chapters** | 7/10 | 8.5/10 (keep) | 8/10 (keep) | **KEEP** (2 of 3 vote to keep story-beat chapters matching locked `v06` chapter cards) |

---

## 1. Title — **KEEP**

- **Decision:** Keep **`How Far Is the Nearest Star?`** (28 characters) unchanged.
- **Why (3 of 3 score `8/10`):** Exact high-intent search question (`THUMBNAIL_AND_TITLE_RULES.md` §1.8), places the familiar noun (`Star`) in the first six words, stays well under the 60-character mobile cutoff, and uses zero hedging or threat clickbait. Because the title asks a direct distance question, all three critics agree the thumbnail must carry the paradox or human-scale shock rather than a literal unit answer.

---

## 2. Thumbnail (`abc_v04`) & 3. Title + Thumbnail Together — **KEEP Original Variant A (`YOU CAN'T SEE IT`) + SELECT `B v04` (`900M YEAR WALK`) OVER `C v04` (`4.2 LIGHT YEARS`)**

### What `abc_v04` Fixed from `J1924` (3 of 3 Agree)
- **Astronomical identity and claim verification:** Both `nearest_star_thumb_B_v04.jpg` (`93f6e2a039e7c761503a26c8b550fcd156849adc31dfd18c65856ae96e61be4c`) and `nearest_star_thumb_C_v04.jpg` (`40eccaf47c5ad885cb964218825e3ca23892e76c82463c83d2b863b5ca68148f`) use the verified ESA/Hubble Proxima Centauri plate (`potw1343a`, crop `[0, 90, 604, 430]`, upscale `2.12× ≤ 2.35×`), with claims checked against locked `v06` captions (`05:15.260–05:23.660` for the 900-million-year continuous walk; `01:42.400–01:48.140` for 4.24 light-years) and `01_Script/SOURCES.md`.
- **Technical gates and `J1924` layout fixes:**
  - Continuous top-edge defocus/dimming (`y ≤ 150` tapering to `y = 220`) clears the top text band (`y = 34..114`) of the upper-left diffraction spike without a flat black slab.
  - Both 3-word hooks (`900M YEAR WALK` with only `900M` yellow; `4.2 LIGHT YEARS` with only `4.2` yellow) sit cleanly in the top band at 11.1% cap height (`80 px` on `720p`) with the bottom-right duration badge clear.
  - Cool-sky/warm-star separation passes `thumb_preview.py --score` above the `120` target (`B v04`: `saturation=132.1, near_black=18%`; `C v04`: `saturation=130.6, near_black=18%`).
  - The Blue Marble Earth reference (`[70, 440, 260, 630]`) is separated cleanly from the lower-left diffraction spike.

### Panel Consensus on `B v04` vs `C v04` and Phone-Size (`168×94`) Layout
1. **Keep Original Variant A (`abc_v01/nearest_star_thumb_A_you-cant-see-it.jpg`, `YOU CAN'T SEE IT`, `sha256: 922855804c4a846fc82f1269d0e524b5b89bde781c187afe5f416367aa970216`) — 3 of 3 agree:**
   - Authorised by `J0833` and preserved across `J1823`/`J1924`. It remains the primary baseline cover (single isolated subject, instant naked-eye invisibility paradox).
2. **Select `B v04` (`900M YEAR WALK`) as the winning challenger hook; reject `C v04` (`4.2 LIGHT YEARS`) — 3 of 3 agree:**
   - **Title + `B v04` (`900M YEAR WALK`) scores `9/10` (`codex.md`), `8/10` (`gemini.md`), and `7.5/10` (`cursor.md`) (2 of 3 `≥ 8/10`):** Translating the title question (*"How Far Is the Nearest Star?"*) into an absurd human journey (`900M YEAR WALK`) creates a genuine curiosity gap against Variant A's invisibility hook (`YOU CAN'T SEE IT`) with zero repeated title words.
   - **Title + `C v04` (`4.2 LIGHT YEARS`) scores `6/10` (`codex.md`), `4/10` (`gemini.md`), and `4.5/10` (`cursor.md`) (3 of 3 `< 8/10`):** All three critics reject `4.2 LIGHT YEARS` because it answers the title question with a textbook number on the thumbnail itself, closing the curiosity loop before the click.
3. **Why all 3 critics score the `168×94` plate `< 8/10` (`7/10`, `7/10`, `6.5/10`), and how that interacts with `J1924` scope:**
   - All three critics flag the same visual tension on the shared `abc_v04` plate: placing the crisp `190×190` Blue Marble Earth cutout (`[70, 440, 260, 630]`, ~25 px wide at `168×94`) beside the large upscaled Proxima diffraction halo (`potw1343a`) plus peripheral blue/purple background stars creates two competing subjects and makes Earth look parked next to an exploding star rather than separated by an immense void.
   - However, `J1924` (`jobs/reviews/J1924.md`) and `J1823` explicitly instructed building `abc_v04` from **both** verified plates (`potw1343a` + Blue Marble Earth separated from the lower spike) to satisfy the `J1766` scale-reference requirement.
   - **Concrete options for Elected Chief ruling in `J1944`:**
     - **Option A (Approve `nearest_star_thumb_B_v04.jpg` as Test & Compare B challenger alongside retained `A`, without a `v05` rebuild):** `nearest_star_thumb_B_v04.jpg` (`900M YEAR WALK`, `sha256: 93f6e2a039e7c761503a26c8b550fcd156849adc31dfd18c65856ae96e61be4c`) meets every binding requirement of `J1924` (`HOOK` PASS: `900M YEAR WALK` with only `900M` yellow; `BAND` PASS: clear top band `y=34..114` free of diffraction spikes; `GRADE` PASS: `sat=132.1`, `near_black=18%`; `PHONE` PASS: readable at `168×94` with duration corner clear; Earth separated from lower spike) and wins 3-of-3 panel preference over `C v04`. If `J1944` requires a 3-way A/B/C set only, `C v04` is technically compliant with `J1924`, or can be omitted in favour of an A vs B (`YOU CAN'T SEE IT` vs `900M YEAR WALK`) test.
     - **Option B (If `J1944` rules to act on the 3-of-3 `168×94` plate critique via `abc_v05` on `J1823`, no spend):** Keep the winning **`900M YEAR WALK`** (`900M` yellow, `YEAR WALK` white) top-band hook on `potw1343a`, either removing the pasted Earth inset (`[70, 440, 260, 630]`) so Proxima is the single isolated subject or shrinking Earth to a tiny bottom-left pinpoint (`≤80×80 px`) while darkening peripheral blue/purple field stars outside the central diffraction halo; if a third variant `C v05` is kept, replace `4.2 LIGHT YEARS` with **`75,000 YEAR TRIP`** (`75,000` yellow, `YEAR TRIP` white, backed by the Voyager 1 speed calculation in Chapter 5 VO).

---

## 4. First 30 Seconds / Short Hook — **KEEP**

- **Decision:** Keep the locked `v06` long cut (`026_NearestStar_v06_cfr18.mp4`) and locked VO unchanged.
- **Why:** All three critics confirm the opening delivers the title question by `0:07.8`, the concrete four-year light-travel distance by `0:13.5`, and the naked-eye invisibility twist by `0:19.7`. Two critics (`codex.md` `7/10`, `gemini.md` `7.5/10`) note that the 12.2-second four-part agenda sentence at `0:20.880–0:33.100` (*"In this film I will show you..."*) slows momentum before naming Proxima Centauri at `0:33.5`, and that the 900-million-year walk lands in Chapter 5 (`05:15.260–05:23.660`); all three explicitly record this as a lesson for future scripts (Standing Lesson 7), not a change to the locked `v06` VO.

---

## 5. Description First Line & Chapters (`11_Upload-Package/Descriptions/nearest_star_long_description_v01.txt`) — **KEEP**

- **Decision:** Keep `11_Upload-Package/Descriptions/nearest_star_long_description_v01.txt` unchanged for this thumbnail review.
- **Why (2-of-3 panel rule):**
  - **First paragraph:** Both `codex.md` and `gemini.md` (2 of 3) vote to keep the first paragraph as written (`How far is the nearest star? Proxima Centauri, a small red dwarf 4.24 light-years away, is so faint you can never see it without a telescope. Even light, the fastest thing there is, takes more than four years to cross the gap.`), noting that it front-loads the exact search query and core entities without spoiling the scale-model or human-journey payoffs.
  - **Chapters:** Both `gemini.md` and `cursor.md` (2 of 3) vote to keep the six story-beat chapter headings (`0:00 How Far Is the Nearest Star?`, `0:33 The Star You Cannot See`, `2:02 Measuring the Gap`, `3:52 Shrink It Down`, `5:12 The Walk`, `6:18 Is Anyone There?`), which obey `AGENTS.md` Reference lessons §2 (*"chapters named as story beats, one per chapter card"*) and match the locked `v06` on-screen chapter cards verbatim (`PACKAGE_MANIFEST.json`).
  - **Advisory note for packaging finish (`J1825`):** `cursor.md` notes that `nearest_star_long_description_v01.txt` does not yet end with the `AGENTS.md` Reference lessons §2.5 one-line production disclosure (*"Pictures: AI-generated scenes alongside NASA/ESA imagery. Facts: every number is checked against the sources listed."*). No package files are modified by `J1943`.

---

## 6. Queued Jobs & Handoff to `J1944`

- **No duplicate build or Studio job is queued by `J1943`:**
  - `J1823` (`026 thumbnails: correct unapproved test variants after J1766 review`) remains the active `026 thumbs` job waiting on the panel + Chief review handoff.
  - `J1944` (`Chief: exact-file ruling on OWB 026 abc_v04 after J1823 fresh panel`, `--after J1943`, `--kind chief`) is already queued in `jobs/queue.json` and becomes immediately claimable by the Elected Chief once `J1943` marks `done`.
  - Per `J1823`, `J1943`, and `J1944`, no live YouTube title, description, manifest, Studio Test & Compare, or `05_Analytics/tests/THUMB_LEDGER.json` changes are made here.
