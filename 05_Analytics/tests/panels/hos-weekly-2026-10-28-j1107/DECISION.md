# Packaging Panel Decision: HOS weekly thumbnail audit (J1107), Periodic Table 002 and later title drafts

**Date:** 2026-10-28
**Job:** J1126 (Claude). Advisory decision; the Chief's PASS stands on this file, and the Chief owns test order.
**Critiques weighed:** `codex.md` (J1123), `gemini.md` (J1124), `cursor.md` (J1125, Gemini covering the Cursor slot while Cursor is out of usage). All three were written independently.
**Hold respected:** J0777 says no new HOS thumbnail B builds until the approved pool has run. Everything below uses existing approved files or text only.

Rule: where two or more critics agree, act on it. Samples are small: Periodic Table has 422 impressions at 3.6% CTR, Atom 789 at 1.0%, X-rays 18 at 0.0%, and none reaches the 1,000-impression bar. These are style-led choices, not proven losers.

---

## 1. Periodic Table thumbnail: do not arm v12. Arm the existing `THE MISSING ELEMENT` v02 instead.

- All three critics score `VACANT CARD SLOT` (v12) 6/10 on its hook copy. It reads as a filing drawer or hardware slot, not a scientific prediction. The plate itself (glowing gap in the wooden grid, Explorer lower left, badge corner clear) is good.
- All three name **THE MISSING ELEMENT** as the fix. Codex proposed the wording; Gemini and the Cursor slot both point to the already-approved file on the same plate. Gemini and the Cursor slot also offer `EMPTY ON PURPOSE` v06, which is kept as the reserve.
- **Decision:** the next Periodic Table thumbnail-only Test & Compare uses **live A vs `08_Thumbnail/Selected/hos_002_thumb_B_missing_element_v02.jpg`**. The title stays fixed and nothing new is built. If that file is missing or fails the phone read at arm time, use `hos_002_thumb_B_empty_on_purpose_v06.jpg`, and say which was used.
- Test order is the Chief's: never replace a running test, and keep the J1113 scheduled Short covers and the protected compilation as they are.

## 2. Titles: no change now. These are later title-only tests, one variable at a time.

| Video | Live (kept for now) | Later title-only B | Why |
|---|---|---|---|
| 002 Periodic Table | How Did We Discover the Periodic Table? | **How Mendeleev's Periodic Table Predicted Missing Metals** | All three score the live title 6/10 as a generic "How did we discover X" formula. Two want "Mendeleev … Predicted Missing Metals" (Codex, Gemini). Two reject the colon label prefix (Gemini, Cursor slot). This wording meets both, keeps both search nouns in the first four words, and is 55 characters. |
| 004 Atom | What's Really Inside an Atom? | **Why Did Particles Bounce Back Off Gold Foil?** | All three say "Sent Particles Back" is weak phrasing. Codex and the Cursor slot both rewrite it as a "why did particles bounce … gold foil?" question. This is the shared core, at 44 characters. Its running paired test is left alone. |
| X-rays | How Did We Discover X-rays? | **X-rays: The Accident That Revealed Our Bones** | Codex and Gemini both score it 8/10. Its active thumbnail test is left alone. |

Run each title test only after that video's thumbnail test has ended, with the thumbnail that is live then held fixed.

## 3. Periodic Table description and chapters: change

Gemini and the Cursor slot agree on two points: the third sentence gives away the Act 5 payoff in the search preview, and the chapter names carry no searchable names. Codex didn't score this because it wasn't given the listing.

- **New opening (replaces sentences 1 to 4):** `Why did Dmitri Mendeleev leave blank gaps in his 1869 periodic table, and dare to predict the weight of metals nobody had ever seen?`
- **Chapters** (same timestamps):
  ```
  0:00 Why the Four Elements Failed
  1:25 Lavoisier, Triads and Newlands' Octaves
  2:49 Measuring Atomic Weight
  4:21 Why Mendeleev Left Empty Gaps (1869)
  6:31 The Discovery of Gallium (1875)
  ```
- The facts reviewer checks the names and dates against the script before the Studio edit: Lavoisier, Newlands' octaves, the 1869 table, and gallium in 1875.

## 4. Not changed here
- **002's locked long cut:** stays locked. Gemini and the Cursor slot agree its opening spends five rhetorical questions before naming Mendeleev or 1869. That is noted as a rule for future scripts (section 6), not a re-cut.
- **Legacy Short covers:** only Gemini raised `29bpGAI0wb8` (`CUT GOLD TO ATOMS?`), so it isn't acted on. It is noted for the next HOS Short cover batch.

## 5. Jobs queued
1. **Studio (Mini, HOS):** arm the Periodic Table thumbnail-only Test & Compare from section 1 when the Chief's test order allows. Check first that no test is running on 002. Add and start the THUMB_LEDGER row only once Studio shows the test armed. Make the description and chapter edits from section 3 after the facts check, and read them back.
2. **Later title-only tests:** queued by that Studio job when each video's thumbnail test ends.

## 6. Rules for PATTERNS.md
- Hook copy must name the mystery, not the prop: "MISSING ELEMENT" beats "VACANT CARD SLOT".
- History of Science long openings: the dated physical fact comes in line one ("In 1869, Mendeleev left an empty box…"), not a run of rhetorical questions.
- Descriptions must not give away the payoff in the first two lines. Chapters should carry names and dates that people search for.
