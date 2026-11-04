# Packaging Panel Decision — OWB 026 (`How Far Is the Nearest Star?` / J1823 v03 Proxima-Only Thumbnail Correction)

- **Date:** 2026-11-04
- **Job:** J1923 (`gemini`, Gemini 4 Argon; advisory packaging panel synthesis — the elected Chief's exact-file decision stands via `J1924`)
- **Evidence reviewed:** Commit `80195a8a72` (`PR #439`, `jobs/reviews/J1823_v03.md`, `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/08_Thumbnail/abc_v03/META.json`, `nearest_star_thumb_B_v03.jpg`, `nearest_star_thumb_C_v03.jpg`, `comparison_true_168x94.png`), `11_Upload-Package/PACKAGE_MANIFEST.json`, `11_Upload-Package/Descriptions/nearest_star_long_description_v01.txt`, and `11_Upload-Package/Captions/nearest_star_long_v06_en-GB.srt`.
- **Critiques weighed:** `codex.md` (J1920), `gemini.md` (J1921), `cursor.md` (J1922, covered by Gemini Argon while Cursor was out of usage). All three critiques are present and were written independently.
- **Rule applied:** Where two or more critics agree (`< 8/10`), act on it; where two or more score `≥ 8/10`, keep. Review only — no live YouTube, Studio, manifest, or `THUMB_LEDGER.json` changes are made by this job.

---

## Summary Table

| Item | `codex.md` (J1920) | `gemini.md` (J1921) | `cursor.md` (J1922) | Panel Consensus |
|---|---:|---:|---:|---|
| **1. Title:** `How Far Is the Nearest Star?` | 8/10 | 8/10 | 7/10 | **KEEP** (2 of 3 score `8/10`; locked per brief) |
| **2. Thumbnail at `168×94`** (`B v03` / `C v03` vs `A`) | B: 7/10 · C: 8/10 | 6/10 | 6/10 (A: 7 · B: 6 · C: 5.5) | **KEEP Original A (`YOU CAN'T SEE IT`) + FIX `B/C` (`abc_v04` distance hooks on `potw1343a`, or `C v03` if Chief rules no v04 rebuild)** |
| **3. Title + Thumbnail Pair** | +B: 7/10 · +C: 8/10 | 7/10 | 6/10 (+A: 8 · +B: 6 · +C: 5) | **KEEP Title + A; replace `PROXIMA HIDES` / `HIDDEN STAR` with `900M YEAR WALK` (B v04) and `4 YEARS OF LIGHT` (C v04)** |
| **4. First 30 Seconds / Short Hook** | 7/10 | 9/10 | 7.5/10 | **KEEP** (locked `v06` VO/cut; note `0:20–0:33` agenda for future scripts only) |
| **5a. Description First Line** | 8/10 | 9/10 | 6/10 | **KEEP** (2 of 3 score `≥ 8/10`) |
| **5b. Description Chapters** | 7/10 | 9/10 | 9/10 | **KEEP** (2 of 3 score `9/10`; matches locked `v06` on-screen chapter cards) |

---

## 1. Title — **KEEP**

- **Decision:** Keep **`How Far Is the Nearest Star?`** (28 characters) unchanged.
- **Why (2 of 3 score `8/10`):** Exact high-intent search question (`THUMBNAIL_AND_TITLE_RULES.md` §1.8), places the familiar noun (`Star`) in the first six words, stays well under the 60-character mobile cutoff, and uses zero hedging or threat clickbait. Because the title is a straight distance lookup question, all three critics agree the thumbnail must carry the paradox or scale shock.

---

## 2. Thumbnail (`abc_v03`) & 3. Title + Thumbnail Together — **KEEP Original Variant A (`YOU CAN'T SEE IT`) + RECOMMEND `abc_v04` Distance-Hook Fix on `J1823`**

### What `abc_v03` Fixed (3 of 3 Agree)
- **Astronomical identity:** Both `nearest_star_thumb_B_v03.jpg` (`de4d3eca9cbfa05f8c583b4e064ae408fcb030177270ee7c546b7efca9ab7968`) and `nearest_star_thumb_C_v03.jpg` (`62c8a813c53a8f1fff098c492a49c7b4b5168eadb26b40a2572f169114721dab`) replace the misidentified Alpha Centauri A/B pair (`GSFC_20171208_Archive_e000214`) with verified ESA/Hubble imagery of Proxima Centauri (`potw1343a`, crop `[0, 126, 604, 466]`, upscale `2.12× ≤ 2.35×`).
- **Technical gates:** Both pass `thumb_preview.py --score` (`B v03`: `saturation=186.4, near_black=3%`; `C v03`: `saturation=116.3, near_black=2%`), keep text to 2 words in the top band (`y=34..114`) with one yellow hook word, include the NASA Blue Marble Earth reference (`[55, 490, 245, 680]`), and keep the bottom-right duration badge clear.

### Panel Consensus on `abc_v03` Weaknesses
1. **Keep Original Variant A (`abc_v01/nearest_star_thumb_A_you-cant-see-it.jpg`, `YOU CAN'T SEE IT`, `sha256: 922855804c4a846fc82f1269d0e524b5b89bde781c187afe5f416367aa970216`) — 3 of 3 agree:**
   - Authorised by `J0833` and preserved by `J1823`/`J1924`. Both `gemini.md` and `cursor.md` select Variant A (`YOU CAN'T SEE IT`) as the strongest overall cover because it challenges the viewer directly in plain English on a clean dark upper-left corner with zero title-word repetition.
2. **Reject Variant B v03 (`PROXIMA HIDES`) — 3 of 3 score `< 8/10` (`7/10`, `6/10`, `6/10`):**
   - All three critics agree that leading with **`PROXIMA`** costs a general viewer a decoding step before the click (the viewer clicks to learn which star is nearest at `0:33` of the film), and B v03's warm brown/orange sky blends into the orange diffraction halo rather than separating the star.
3. **Reject Variant C v03's `HIDDEN STAR` copy and identical-angle test setup — 2 of 3 score `< 8/10` (`gemini.md` `6/10`, `cursor.md` `5.5/10`; `codex.md` `8/10`):**
   - **Rule violation (`THUMBNAIL_AND_TITLE_RULES.md` §2.3):** `HIDDEN STAR` repeats the word **`STAR`** directly from the 6-word title *How Far Is the Nearest **Star**?* (*"The thumb adds to the title. It never repeats it"*).
   - **Collapsed A/B/C test matrix:** With Variant A already testing naked-eye invisibility (`YOU CAN'T SEE IT`), turning B and C into `PROXIMA HIDES` and `HIDDEN STAR` makes all three covers test synonyms for "invisible" on the exact same `potw1343a` starburst plate, leaving the title's **"How Far"** question completely untested.
   - **Visual/text friction at `168×94`:** All three critics note that a frame-filling white-orange diffraction starburst visually fights "hides/hidden" at a glance; `gemini.md` and `cursor.md` also flag the upper-left diffraction spike cutting directly through the top text band (`OXI` / `DDEN`) and the lower-left spike running straight beneath the hard-edged Earth cutout (`[55, 490, 245, 680]`).
4. **Keep C v03's deep-blue sky separation over B v03's warm brown field — 2 of 3 agree (`codex.md`, `gemini.md`):**
   - C v03's cool deep-blue background separates the warm orange Proxima plate (`potw1343a`) much more cleanly than B v03's orange-on-orange field while still passing the `≥100` saturation floor (`116.3`, near-black `2%`).

### Recommended Thumbnail Action for `J1924` (Elected Chief Exact-File Ruling)
- **Primary recommendation (2-of-3 panel consensus — `FIX` on `J1823` to build `abc_v04`, no spend, from existing verified plates `potw1343a` + `GSFC_20171208_Archive_e002130`):**
  - **Variant A (keep unchanged):** `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/08_Thumbnail/abc_v01/nearest_star_thumb_A_you-cant-see-it.jpg` (`YOU CAN'T SEE IT`).
  - **Variant B v04 (primary Test & Compare B challenger): `900M YEAR WALK`** (`900M` in house yellow, `YEAR WALK` in house white — 3 words, top band `y=34..114`, zero words repeated from `How Far Is the Nearest Star?`; pits the visceral human-scale walk time from Chapter 5 VO against A's invisibility hook) over the verified `potw1343a` Proxima plate on C v03's high-contrast deep-blue background grade (or a cool-sky/warm-star grade with `saturation ≥ 120`, `near_black ≤ 30%`), darkening the upper-left diffraction spike behind the top text band (`y=0..130`) and attenuating the lower-left spike / adding a subtle dark outer rim around the Earth inset (`[55, 490, 245, 680]`) so Earth separates cleanly across a dark gap.
  - **Variant C v04 (third slot for A/B/C completeness): `4 YEARS OF LIGHT`** (`4 YEARS` in house yellow, `OF LIGHT` in house white — or `4.2 LIGHT YEARS` with `4.2` yellow; 3 words, top band `y=34..114`, zero repeated title words; tests the light-travel answer from `0:13` VO) on the verified `potw1343a` Proxima plate with the same top-band spike darkening and Earth separation.
- **Fallback if Elected Chief in `J1924` rules no v04 rebuild is needed:**
  - Between the two existing `abc_v03` candidates, **`nearest_star_thumb_C_v03.jpg` (`HIDDEN STAR`, cool blue sky, `sat=116.3, near_black=2%`, `sha256: 62c8a813c53a8f1fff098c492a49c7b4b5168eadb26b40a2572f169114721dab`)** is strictly preferred over `nearest_star_thumb_B_v03.jpg` (`PROXIMA HIDES`), though 2 of 3 critics flag `HIDDEN STAR` for repeating `STAR` from the title (`THUMBNAIL_AND_TITLE_RULES.md` §2.3).

---

## 4. First 30 Seconds / Short Hook — **KEEP**

- **Decision:** Keep the locked `v06` long cut (`c5AdqQsnnys`) and locked VO unchanged.
- **Why:** All three critics confirm the opening asks the title question by `0:07.8`, gives the concrete four-year light-travel distance by `0:13.5`, and lands the naked-eye invisibility twist by `0:19.7`. Two critics (`codex.md` `7/10`, `cursor.md` `7.5/10`) note that the 12.2-second four-part agenda at `0:20.8–0:33.1` (*"In this film I will show you..."*) softens momentum before naming Proxima Centauri at `0:33.5`; both explicitly record this as a lesson for future scripts (Standing Lesson 7), not a change to the locked `v06` cut.

---

## 5. Description First Line & Chapters (`11_Upload-Package/Descriptions/nearest_star_long_description_v01.txt`) — **KEEP**

- **Decision:** Keep `11_Upload-Package/Descriptions/nearest_star_long_description_v01.txt` unchanged.
- **Why (2-of-3 panel rule):**
  - **Description first line:** Scored **`8/10`** (`codex.md`) and **`9/10`** (`gemini.md`) vs `6/10` (`cursor.md`). Two of three critics score it `≥ 8/10` and vote to keep because repeating the exact search query (`How far is the nearest star?`) and naming `Proxima Centauri`, `red dwarf`, `4.24 light-years away`, naked-eye invisibility, and the four-year light travel time serves search intent while preserving the scale-model and travel-time payoffs.
  - **Chapters:** Scored **`9/10`** (`gemini.md`) and **`9/10`** (`cursor.md`) vs `7/10` (`codex.md`). Two of three critics score the chapters `9/10` and vote to keep because the six headings (`0:00 How Far Is the Nearest Star?`, `0:33 The Star You Cannot See`, `2:02 Measuring the Gap`, `3:52 Shrink It Down`, `5:12 The Walk`, `6:18 Is Anyone There?`) follow `AGENTS.md` Reference lessons §2 (*"chapters named as story beats, one per chapter card"*) and match the locked `v06` on-screen chapter cards verbatim.

---

## 6. Queued Jobs & Governance Boundaries

- **No duplicate build or Studio job queued here:**
  - `J1823` (`026 thumbnails: correct unapproved test variants after J1766 review`) is already the active `026 thumbs` job on hold (`Complete queued panel J1920-J1922, decision J1923 and exact-file ruling J1924; no rebuild unless FIX`).
  - `J1924` (`Chief: exact-file decision on OWB026 J1823 v03 after packaging panel`, `--after J1923`, `--kind chief`) is already queued to inspect the exact `abc_v03` files alongside this `DECISION.md` and record either an exact-file `PASS` or a concrete `FIX` on `J1823`.
  - Per `J1823`, `J1923`, and `J1924`, no live title, manifest, Studio Test & Compare, or `05_Analytics/tests/THUMB_LEDGER.json` changes are authorised at this stage.

## Elected-Chief ruling — J1924, 4 November 2026

Codex: **FIX B/C v03; preserve original A.** Exact-file findings and binding correction scope are in `jobs/reviews/J1924.md`. J1823 resumes ready no-spend abc_v04 work: proposed B `900M YEAR WALK` (900M yellow), proposed C `4.2 LIGHT YEARS` (4.2 yellow), with claim verification, clear text space, cool separation, gates and fresh panel/Chief review. These replace the four-word C suggestion above. The ruling does not treat a repeated noun alone as title duplication. PR439 is merged as historical evidence, not image approval. No live packaging changes authorised.
