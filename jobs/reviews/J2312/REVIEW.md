# J2312 Review — OWB 026 `HZGTovJu_TQ` (`mon16_cant_see_nearest_star`) E1 Recorded-Word Conflict

- **Job:** `J2312` (`OWB 026 E1 recorded-word conflict: decide J2307 recipe or retain original`)
- **Parent Job:** `J2307` (`OWB 026: E1 local re-cut for HZGTovJu_TQ; preserve scheduled copy`, `1/3`)
- **Film / Slot:** `OWB:026` (`02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star`), YouTube ID `HZGTovJu_TQ`, scheduled `2026-11-16T11:30:00Z` (`Mon 16 Nov 2026 11:30 London`)
- **Reviewer:** `macbook` (`gemini-argon`, text feasibility review; no capability-only hold)
- **Reviewed Evidence:**
  - PR #591 (`a6b61c018fdf2c4fb80a0023ef5e98308fd6f0eb`), `jobs/reviews/J2307/PREFLIGHT.md`
  - `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/words.json` (`mon16_cant_see_nearest_star_vo_v01_LOCK.mp3`, SHA-256 `556a5f4a67fe96f76ecfeeb51dfb9831a10b2ff00e1f62695304ed55cd08dcee`, `24.48 s`, `53` words)
  - `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/words.json` (`nearest_star_vo_v01.wav`, `491.02 s`, `90` sentences)
  - `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/words.json` (`21.60 s`)
  - `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/fri20_grapefruit_cherry/words.json` (`20.64 s`)
  - `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/026_nearest_star_pickup_nextweek_v01_NOTE.md` (`2.96 s`)
  - `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/_assemble_mon16_cant_see_nearest_star_v03.py`
  - `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports/mon16_cant_see_nearest_star_v03_meta.json`, `cuts_v03.json`, and `mon16_cant_see_nearest_star_v03_infeasibility.json`
  - `jobs/reviews/J0935/RULING_2026-10-26_CODEX.md` and `jobs/reviews/J0935/RULING_2026-10-28_GEMINI.md`
  - `.cursor/rules/orbit-build-shorts.mdc` (`OWB-2026-11-E1` and `Keeper score`)

---

## 1. Verdict Summary (`KEEP` Scheduled Original `v01` / Close `J2307` Local Experiment)

| Item | Ruling | Summary |
|---|---|---|
| **1. `J2307` Preflight & Conflict Evidence (`PR #591` / `a6b61c018f`)** | **`KEEP` (Verified)** | `HZGTovJu_TQ` reads `private`, `publishAt: 2026-11-16T11:30:00Z`, `madeForKids: false`, title *"If You Can't See the Nearest Star, How Far Away Is It?"*, with preserved `v01` SHA-256 `24a5552baec19feec7ec45e47f0e3ce3d6b2a3309b7ad935c32309220b03b5ad` (`22,676,672` bytes) verified in `UPLOADS.json` and `J0851_READBACK.json`. |
| **2. Existing-Recording E1 Recipe Search Across Entire `026` VO Corpus** | **`NO-GO` (`0` Compliant Recipes)** | Exhaustive audit of `mon16` Short VO (`53` words), `026` long VO (`90` sentences), `wed18`, `fri20`, and `pickup_nextweek_v01` confirms that **no recorded sentence or grammatical splice satisfies both the retained Keeper first-line question requirement and E1's `<= 1.50 s` surprise timing** under house tempo limits (`<= 1.06x` / `<= 1.08x`) and `£0` / no-new-TTS. |
| **3. Scheduled Original `HZGTovJu_TQ` (`mon16_cant_see_nearest_star_v01.mp4`) & Parent `J2307`** | **`KEEP SCHEDULED ORIGINAL` / Close `J2307`** | Do not silently extend the Test A waiver to this standalone Short, do not waive a failed gate, and do not re-render `v03` (`OPEN_TEMPO=1.42`, declarative opener, `Cut 2 = 5.905 s > 4.80 s`). Retain scheduled `v01` (`HZGTovJu_TQ`, `24a5552b...`) untouched for `2026-11-16T11:30:00Z` and close `J2307` as `done` (retaining its `1/3` preflight progress record). |

---

## 2. Exhaustive Audit of `026` Recorded VO Corpus Against `OWB-2026-11-E1` + `Keeper Score`

### A. Governing Rules (`OWB-2026-11-E1` + `Keeper Score`)
1. **Keeper First-Line Question Lock Retained:** Under `.cursor/rules/orbit-build-shorts.mdc` → `OWB-2026-11-E1` (*"Keep Keeper length/question rules, payoff >=70%, the one teaching overlay, Related/description link, SFX and all existing ship gates. Existing Test A exemptions and explicit per-cut waivers remain in force: record conflicts for review rather than silently changing the test arm or calling an exception a full E1 PASS"*):
   - `HZGTovJu_TQ` (`mon16_cant_see_nearest_star`) is a standalone recorded Short (`mon16_cant_see_nearest_star_vo_v01_LOCK.mp3`), **not** 026's Test A opening lift (`026`'s Test A replacement is `aAUgIGEuPwQ`, delivered under `J1101` for `A6TW_6CXhcs`).
   - It holds no explicit first-line question waiver (`RULING_2026-10-26_CODEX.md`, `RULING_2026-10-28_GEMINI.md`, `jobs/briefs/J2207/INVENTORY.md`).
   - Therefore, Spoken Line 1 must ask the preserved title question (*"If You Can't See the Nearest Star, How Far Away Is It?"*, or a compliant non-anaphoric question matching the preserved title) with first word `<= 0.15 s`, planet/star named in `0–2.5 s`, and the spoken surprise (`"can't see"` / `"cannot see"`) landing by **`<= 1.50 s`**.
2. **Zero Spend / Existing Recordings Only:** `£0`, no new ElevenLabs TTS, no invented or clipped speech, and no tempo distortion beyond house limits (`1.06x` normal ceiling; `1.08x` strict Batch B cap per `RULING_2026-10-26_CODEX.md`).

### B. Audit of Recorded `mon16` Short VO (`mon16_cant_see_nearest_star/words.json`)
Full recorded text (`24.48 s`, `53` words):
> *"The nearest star to the Sun is out there tonight. You can't see it. It's called Proxima Centauri, a small red dwarf. It gives out less than 1% of the Sun's light. Its light still takes more than four years to reach you. The full film, How Far Is The Nearest Star?"*

1. **Preserved Title Question Absent:** Neither *"If You Can't See the Nearest Star, How Far Away Is It?"* nor the pre-retitle script question (*"Why Can't You See the Nearest Star?"*) was ever recorded in `mon16_cant_see_nearest_star_vo_v01_LOCK.mp3`.
2. **Recorded Opening (`0.100–5.240 s`) Fails Both Keeper Line-1 Question and Raw/Capped `<= 1.50 s` Surprise:**
   - Sentence 1 (`0.100–3.340 s`, duration `3.240 s` raw / `3.057 s` @ `1.06x` / `3.000 s` @ `1.08x`): *"The nearest star to the Sun is out there tonight."*
   - Breath (`3.340–4.280 s`): `0.940 s`.
   - Sentence 2 (`4.280–5.240 s`, duration `0.960 s` raw): *"You can't see it."* (`"can't"` at `4.420–4.660 s`).
   - Even if `"is out there tonight"` (`1.940–3.340 s`) is excised to form *"The nearest star to the Sun — you can't see it"* (`0.06–1.84 s` + `4.22–5.30 s`), that opening is a **declarative statement, not a question**, violating the retained Keeper line-1 question lock (`keeper_line1_question_compliant: false`). Moreover, at `1.00x–1.08x` tempo, `"The nearest star to the Sun"` (`0.100–1.780 s` = `1.680 s` raw / `1.585 s` @ `1.06x` / `1.556 s` @ `1.08x`) plus a `0.050 s` join gap places `"You"` at `1.606–1.730 s` and `"can't"` at `1.735–1.870 s` (`> 1.50 s`). Earlier `v03` (`_assemble_mon16_cant_see_nearest_star_v03.py`) only reached `"can't"` at `1.445 s` by forcing `OPEN_TEMPO = 1.42` (`42%` speedup), which violates the `<= 1.08x` tempo cap (`RULING_2026-10-26_CODEX.md`).
3. **Recorded Closing Question (`20.940–24.440 s`) Fails Meta-CTA Lock, Title-Question Match, and `<= 1.50 s` Surprise:**
   - *"The full film, How Far Is The Nearest Star?"* (`20.940–24.440 s`) is the forbidden closing meta-CTA (`OWB-2026-11-E1`: *"Zero meta-promise, spoken CTA or end card"*).
   - Extracting its question half *"How Far Is The Nearest Star?"* (`22.440–24.440 s`, duration `2.000 s` raw / `1.887 s` @ `1.06x` / `1.852 s` @ `1.08x`) asks a different question than the preserved title (*"If You Can't See the Nearest Star, How Far Away Is It?"*), omits the `"can't see"` premise in sentence 1, and already spans `1.852–2.000 s` before any second clause can start, pushing `"can't"` to `~3.30 s` (`> 1.50 s`).

### C. Audit of All Questions & Candidate Clauses in `026` Long VO (`02_Voiceover/words.json`, 90 Sentences) & Other `026` Shorts
Every question recorded across all `90` sentences of `026/02_Voiceover/words.json` (`491.02 s`), `wed18` (`21.60 s`), `fri20` (`20.64 s`), and `pickup_nextweek_v01` (`2.96 s`) was checked:

| Source & Sentence | Timestamp (s) | Raw Dur (s) | Dur @ `1.06x` / `1.08x` (s) | Verbatim Text | Why It Cannot Form a Compliant `HZGTovJu_TQ` E1 Opener |
|---|---:|---:|---:|---|---|
| `long S02` | `5.620–7.440` | `1.820` | `1.717` / `1.685` | *"So how far away is the nearest one?"* | Anaphoric (`"the nearest one"`, failing the J0900/J0907 rule that sentence 1 must name the star/subject directly); does not match the preserved title question; duration (`1.685–1.820 s`) already exceeds `1.50 s` before *"You cannot see that star at all"* (`S05`, `15.880–19.340 s`, `"cannot"` at `1.84 s` @ `1.08x`). |
| `long S23` | `122.140–125.300` | `3.160` | `2.981` / `2.926` | *"How do you measure the distance to something you can never visit?"* | Different question; `2.926–3.160 s` (`> 1.50 s`) before any surprise word; does not name the nearest star. |
| `long S50` | `263.860–265.480` | `1.620` | `1.528` / `1.500` | *"Now, where is the nearest star?"* | Mid-argument transition from the grapefruit/cherry scale section; does not match the preserved title question; consumes `1.500–1.620 s` before any `"can't see"` surprise word can start (`> 1.50 s`). |
| `long S56` | `296.400–298.060` | `1.660` | `1.566` / `1.537` | *"And our farthest spacecraft?"* | Unrelated Voyager transition fragment (`> 1.50 s`). |
| `long S60` | `312.280–314.400` | `2.120` | `2.000` / `1.963` | *"So how long would the journey take?"* | Unrelated travel-time question (`> 1.50 s`); anaphoric. |
| `long S71` | `378.984–381.204` | `2.220` | `2.094` / `2.056` | *"So what is waiting at the end of the journey?"* | Unrelated Proxima b transition (`> 1.50 s`). |
| `long S80` | `421.904–423.104` | `1.200` | `1.132` / `1.111` | *"Could we ever go and look?"* | Unrelated Starshot question; anaphoric (`"go and look"`). |
| `long S88` | `469.324–475.684` | `6.360` | `6.000` / `5.889` | *"What if the most important thing about the nearest star is not how close it is but how far?"* | Closing philosophical question (`5.889–6.360 s > 1.50 s`). |
| `wed18` Q1 | `4.420–6.960` | `2.540` | `2.396` / `2.352` | *"Could a robot like it reach the nearest star?"* | Unrelated Voyager question (`wed18`); anaphoric (`"like it"`); `> 2.35 s`. |
| `fri20` Q1 | `8.620–9.200` | `0.580` | `0.547` / `0.537` | *"Where is it?"* | Anaphoric (`"it"`); unrelated cherry scale question (`fri20`). |
| `pickup_v01` | `0.000–2.960` | `2.960` | `2.792` / `2.741` | *"Next week, what if Earth stopped spinning?"* | Unrelated 027 teaser pickup. |

- **Sub-Clause / Word-Level Splice Check:**
  - The word `"why"` occurs only once in the entire `026` VO corpus, inside declarative sentence `long S09` (`44.580–49.240 s`: *"That is why you will never spot it by eye, even on the darkest night"*, `"why"` at `45.280–45.480 s` with mid-clause declarative cadence).
  - The word `"if"` occurs only three times in `026` (`long S06` *"if you shrink"*, `long S86` *"If someone there answered"*, and `long S88` *"What if the most important thing"*), never followed by *"you can't see"*.
  - Stitching isolated words across unrelated declarative sentences to synthesize *"If you can't see the nearest star, how far away is it?"* or *"Why can't you see the nearest star?"* would produce clipped phonemes, mismatched pitch/falling-to-rising intonation welds, and still exceed `1.50 s` (`7–12` words > `2.0 s`), violating the `J2307` brief (*"If recorded words cannot meet a requirement, report exact conflict for reviewer, do not invent speech"*) and `RULING_2026-10-26_CODEX.md` / `RULING_2026-10-28_GEMINI.md`.

### D. Why Earlier `J0935` `mon16_cant_see_nearest_star_v03` (`cddcfb96...`) Remains Ineligible Under E1
1. **Non-Question Opener (`keeper_line1_question_compliant: false`):** `v03` opens with the declarative statement *"The nearest star to the Sun — you can't see it"*, which failed Keeper Rule 1 in `RULING_2026-10-28_GEMINI.md` (`NO RECUT (RETAIN SCHEDULED v01)`).
2. **Unacceptable Tempo Distortion (`1.42x` / `1.18x` / `1.10x`):** `_assemble_mon16_cant_see_nearest_star_v03.py` sets `OPEN_TEMPO = 1.42` on `0.06–1.84 s`, `MID_TEMPO = 1.18` on `128.06–148.30 s`, and `1.10x` on `5.94–14.94 s`, violating the `<= 1.08x` tempo cap (`RULING_2026-10-26_CODEX.md`).
3. **E1 Cut 2 Violation (`5.905 s > 4.80 s`):** In `cuts_v03.json`, `s00` runs `0.000–2.550 s` (`Cut 1 = 2.550 s <= 2.80 s`), and `s01` runs `2.550–5.905 s` (**`Cut 2 = 5.905 s > 4.80 s` E1 limit**).

---

## 3. Disposition & Parent Update (`J2307`)

1. **Explicit E1 No-Go for `HZGTovJu_TQ` (`mon16_cant_see_nearest_star`):**
   - No compliant existing-recording recipe exists for `HZGTovJu_TQ`.
   - Consistent with `J2314` / `J2308` (`cwU_0WWeNZ4`, `1d6c314047`) and `RULING_2026-10-28_GEMINI.md`, the local E1 re-cut experiment `J2307` is **closed as `done` (explicit E1 no-go)** with its `1/3` preflight verification progress preserved.
2. **Scheduled Original Preserved Untouched:**
   - `HZGTovJu_TQ` (`mon16_cant_see_nearest_star_v01.mp4`, SHA-256 `24a5552baec19feec7ec45e47f0e3ce3d6b2a3309b7ad935c32309220b03b5ad`, `private`, `publishAt: 2026-11-16T11:30:00Z`) remains the scheduled upload in `UPLOADS.json` and YouTube Studio.
   - `J0861` continues to own the post-public Related video + pinned comment follow-through after the `026` long (`c5AdqQsnnys`) goes public on `15 Nov 2026 18:00Z`.
   - `£0` spent; zero media renders, zero YouTube API writes, zero Buffer changes.
