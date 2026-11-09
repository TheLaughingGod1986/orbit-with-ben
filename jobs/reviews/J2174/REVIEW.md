# J2174 Review Decision — HOS 005 `s06_blood_pressure_cuff` Bounded Rule-8 Opening & Clinical-Source Repair

- **Job:** `J2174` (ref `J2168`, repo `hos`, film `005`, stage `edit`, kind `review`)
- **Reviewer:** `gemini` (`gemini-4-argon-high`, fallback lane 3 of 4)
- **Date:** 2026-11-05
- **HOS Commit & PR:** `f7f544fb` on branch `gemini/J2174-cuff-decision` (PR [#412](https://github.com/TheLaughingGod1986/history-of-science/pull/412), building on `J2168` commit `7a695f0e` on `codex/J2168-qualification`, also pushed to `origin`); `bash 00_Brand/Channel-Setup/tools/check_all.sh` → `ALL CHECKS PASS`.
- **Verdict:** **FIX / NO-GO for £0 unchanged-word assembly (`v02` not queued).**

## 1. Clinical-Method Source Repair (`01_Script/FACT_NOTES_v01.md` Row 38)

Repaired `01_Script/FACT_NOTES_v01.md` row 38 from `"Any clinical-methods text."` to the primary American Heart Association (AHA) Scientific Statement on human blood pressure measurement, with exact verbatim quotes distinguishing manual auscultatory measurement from automated oscillometric cuffs:

- **Source:** T. G. Pickering et al., *"Recommendations for Blood Pressure Measurement in Humans: An AHA Scientific Statement from the Council on High Blood Pressure Research Professional and Public Education Subcommittee"*, *The Journal of Clinical Hypertension* 7(2):102–109 (2005), DOI `10.1111/j.1524-6175.2005.04377.x`, PMID `15722655`, https://pmc.ncbi.nlm.nih.gov/articles/PMC8109470/
- **Manual Auscultatory Method (Korotkoff, 1905) — exact quote:**
  > *"The brachial artery is occluded by a cuff placed around the upper arm and inflated to above systolic pressure. As it is gradually deflated pulsatile blood flow is reestablished and accompanied by sounds that can be detected by a stethoscope held over the brachial artery just below the cuff. The onset of phase I of the Korotkoff sounds (tapping sounds corresponding to the appearance of a palpable pulse) corresponds to systolic pressure, but tends to underestimate the systolic pressure recorded by direct intra‐arterial measurement."*
- **Automated Oscillometric Technique — exact quote:**
  > *"When the oscillations of pressure in a sphygmomanometer cuff are recorded during gradual deflation, the point of maximal oscillation corresponds to the mean intra‐arterial pressure. The oscillations begin above systolic BP and continue below diastolic BP, so that systolic and diastolic BPs can only be estimated indirectly according to some empirically derived algorithm. One advantage of the method is that no transducer needs to be placed over the brachial artery, so placement of the cuff is not critical."*
- **Distinction:** The locked script line (*"It squeezes until the blood stops getting in, then lets go, and listens for the moment it starts to flow again"*) describes **manual auscultatory sphygmomanometry** (stethoscope detection of Phase I Korotkoff sounds upon resumed pulsatile flow after brachial artery occlusion), whereas automated electronic cuffs sense cuff-wall pressure oscillations around mean intra-arterial pressure rather than listening for acoustic sounds.

## 2. Bounded £0 Unchanged-Word Opening Proof (Why No £0 Assembly Is Lawful)

In `02_Voiceover/part05_the_vessels_he_never_saw_v01_raw_align.json` (`8313148b8040...`), the entire blood-pressure cuff passage (`indices 178–220`, `80.740–95.440 s`) is **43 words** and **14.700 s** raw (`14.513 s` pause-capped):
- `178–192` (`80.740–85.200 s`, `4.460 s`, 15w): *"And the next time a nurse wraps a cuff round your arm, think of Harvey."*
- `193–199` (`85.560–88.080 s`, `2.520 s`, 7w): *"A blood pressure cuff is his band."*
- `200–220` (`88.267–95.440 s`, `7.173 s`, 21w): *"It squeezes until the blood stops getting in, then lets go, and listens for the moment it starts to flow again."*

Every candidate unchanged-word window fails one or more mandatory rules:
1. **Existing `v01` lift (`107–126` + `178–220`, 63w, `23.667 s` VO):** Sentence 1 (`0.000–8.304 s`) is generic circulation (*"Your blood leaves your heart..."*); `"cuff"` is not spoken until `~10.81 s`. Fails `LEARNINGS.md` Rules 2 & 8.
2. **Start at `178` (*"And the next time a nurse wraps a cuff round your arm, think of Harvey."*):** Opens with a continuation conjunction (`"And the next time..."`), delays `"cuff"` to `2.044 s > 1.50 s`, has no surprise claim in sentence 1 (`LEARNINGS.md` Rules 2 & 8 FAIL), and is only **43 words / `14.513 s` VO** (fails HOS `55–65`w and `22.0–27.0 s` locks). Extending into `221–251` (*"A sum, a band, and a row of little doors..."*) reaches **74 words** (`>65` cap), finishes the cuff mechanism at `14.51 s` (`54% < 70%`, failing `LEARNINGS.md` Rule 6 payoff withholding), and turns the final `11.8 s` into a generic recap of Harvey's 1628 experiments.
3. **Start at `193` (*"A blood pressure cuff is his band."*):** Leaves `"his band"` anaphoric/pronoun-broken at `0.0 s` with `"Harvey"` unnamed (`LEARNINGS.md` Rule 2 FAIL) and is only **28 words / `9.880 s` VO**; non-chronological sentence splicing is barred without new line/splice approval.
4. **Visual plate constraint:** Part 05 holds only two 8.0 s modern-cuff plates (`13_cuff_t1.mp4`, `14_cuff_release_t1..t4.mp4`). Under `LEARNINGS.md` Rule 3 (`change something every 2.5–4 s`, max hold `≤3.8 s`) and `picture_qa.py`, filling `22–27 s` without reusing Part 04 ligature plates from `PFj6172YU4Q` (`s02_the_tied_arm`, 8 Nov) requires additional modern-cuff visual coverage.

## 3. Exact Missing Inputs & Recipe If Chief Later Scopes `v02`

- **Missing Input 1:** Approved standalone Short script (`58–62` words, positive question title `How Does a Blood Pressure Cuff Work?`, sentence-1 subject + surprise by `1.50 s` with `≤0.15 s` VO onset and no unresolved pronoun, `<0.25 s` seam at `4–5 s`, manual auscultatory Korotkoff mechanism payoff starting at `≥70%` runtime, zero meta-promise) + 1 new ElevenLabs VO take (`vo_take.py`).
- **Missing Input 2:** 2–3 additional modern-cuff / brachial-artery occlusion / stethoscope auscultation visuals (either £0 house-style inked teach graphics via `--kind chart` or Chief-scoped Flow Veo 3.1 plates).
- **Recipe locks:** Frame 0 on moving `13_cuff_t1.mp4` (`in_s=1.00, crop_x=420`, first cut `≤3.0 s`, concrete hook `STOPS YOUR **BLOOD**` or `SQUEEZES IT **SHUT**`); `9.0–14.0 s` parent-title banner `The Tied Arm That Proved Your Blood Circulates` (payoff withheld past `14.0 s`); at most 1 educational overlay in `[656, 1264]` (`WILLIAM HARVEY · London, 1628` or `NIKOLAI KOROTKOFF · 1905`); `1.00 s` (`≤1.50 s`) loop return to `13_cuff_t1.mp4` with `no_cta: true` (no end-card/CTA in the last `2.0 s`); distinct music bed + house SFX (`sfx_kit.py level` PASS), AAC `-14.0 ± 0.5 LUFS` / `≤ -1.6 dBTP`, passing all current gates before any `awaits`.
- **Slot status:** Conditional **10 November 11:30** and **10 December** (`s07` rejected in `J2168`; `s08` excluded; no extra `007`) remain **unfilled**.
