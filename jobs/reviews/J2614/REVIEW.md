# J2614 QA Review — HOS 008 `hos_008_master_v04.mp4` Salon Splice (Timeline Frames 2560..2665)

- **Reviewer:** `gemini` (`gemini-argon`)
- **Date:** 2026-11-14
- **Target Master:** `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_precheck/master_v04/hos_008_master_v04.mp4`
  - **SHA-256:** `735ac816e00ba4a2690494bfeb9fddecfdeaa2f60417c5192f48155a9333db31` (`2,847,983,180` bytes)
- **Verdict:** **FIX / PARKED FOR CHIEF** (Question 2 is **NO** — the 20-frame `f000` hold at `2586..2605` reads as a `0.833 s` static freeze; additionally, `2505 -> 2506` still applies the `1.12x` crop that Chief withdrew in desk comment `6796274013`).

---

## 1. Contact Sheets & Evidence Artifacts

Saved on `studio-live` under `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_precheck/master_v04/J2614/` (and in `/Volumes/MiniWork/scratch/J2614-work/`):

1. **Half-Second Sheet + Cut-In Pair + Spark Window Zoom (`2560..2665` + `2666`):**
   - Path: `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_precheck/master_v04/J2614/J2614_salon_splice_half_second_sheet.jpg`
   - SHA-256: `90c276ebbe2199282d200ae6f7316a96a4ba50db88dc892e5d42ff8d93826fab`
2. **All-107-Frames Contact Sheet (`2560..2666`):**
   - Path: `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_precheck/master_v04/J2614/J2614_salon_splice_all_106_frames.jpg`
   - SHA-256: `6ae1755801cc2e19f2e89f83a40ee8696b94ef55d5354592ba41dd9fb1a22e2c`
3. **Cut [22] → Cut [23] Boundary Pair (`2505` vs `2506`):**
   - Path: `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_precheck/master_v04/J2614/pair_2505_2506.jpg`
   - SHA-256: `6d4730f27e24b14b96e34d23a267905913fc3e35d3b73fead3ea65d4770fe3fa`
4. **Frame-by-Frame Diff & Source Mapping Metrics (`2560..2665`):**
   - Path: `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_precheck/master_v04/J2614/metrics.json`
   - SHA-256: `14413fcc54e867868c08f4d5fc25f8f517ecd81ce29f0a68abaf99496a9ccc6a`

---

## 2. Answers to the Four J2614 Questions

### Q1. Is the cut from the tube plate into take 4 a clean cut-in: the same room, the same two people, no jump?
- **At `2585 -> 2586` (tube tail into take 4): YES (as a scene/cut-in transition).**
  - Frame `2585` (`107.96 s`, last frame of `01_salon_tube_t1.mp4` tail, source `f178`) shows the wide over-the-shoulder view of the lecturer in the dark green coat and white cuff raising the vertical glass tube before the seated salon audience in the wood-panelled room with tall windows on the right and framed portraits on the wall.
  - Frame `2586` (`108.00 s`, first frame of `02_salon_spark_j2241_t4_J2592_v01.mp4` `f000`) cuts into the medium two-shot in the wood-panelled parlour: the lady in the cream lace dress and powdered wig on the left holding her knuckle toward the glass tube held by the lecturer in the dark green coat and white cuff/cravat on the right.
- **Note on the earlier `2505 -> 2506` join (cut [22] into cut [23] tube tail): JUMP PRESENT.**
  - In `_j2242_salon_patch.py`, frames `2506..2585` still apply `crop=iw*0.89:ih*0.89:iw*0.08:ih*0.06` (`1.12x` closer crop) from desk comment `6796013653`. Chief withdrew that crop in desk comment `6796274013` (*"The 1.12× crop in comment 6796013653 is withdrawn. Frames 98 and 99 are one rub, and the crop jumps the scale. Play the tail full frame."*). As shown in `pair_2505_2506.jpg`, `2505 -> 2506` jumps `1.12x` in scale mid-rub between source frames `98` and `99`.

### Q2. Does the hold at the head of take 4 read as moving picture, not as a freeze?
- **NO — it reads as a static freeze (`20` identical frames = `0.833 s`).**
  - `_j2242_salon_patch.py` used `tpad=start=19:start_mode=clone` before `f000..f060` (`schedule = [0] * 19 + list(range(61))`). Because `f000` follows the 19 cloned copies of `f000`, timeline frames **`2586..2605` are `20` consecutive copies of `f000`** (`20 / 24 = 0.8333 s`, from `108.000 s` to `108.792 s`), exceeding even the `0.80 s` freeze limit.
  - Across frames `2588..2605`, decoded frame-to-frame pixel differences are literally zero (`mean_abs_diff = 0.0000`, `max_abs_diff = 0`), and `2586..2588` differ only by H.264 QP1 rounding (`mean_abs_diff <= 0.0022`, `max_abs_diff <= 3`).
  - Visually in `v04_salon_2560_2665.mp4` and on `J2614_salon_splice_half_second_sheet.jpg`, the lady and lecturer freeze completely still for `0.833 s` (`2586..2605`) after the cut-in before motion suddenly starts at frame `2606` (`src f001`, `mean_abs_diff = 1.4817`).
  - Per desk ruling `6796013653` / J2242 brief: *"If the hold reads as a freeze, spread it as a gentle slow of `f000`–`f012` instead, keeping `f030` on 2635"* (or use Chief's fallback: the clean first two seconds of take 3 with the spark on a cut).

### Q3. Is the spark on timeline frame 2635, and nowhere else?
- **YES (matches the approved J2592 3-frame spark composite `02_salon_spark_j2241_t4_J2592_v01.mp4`, passed in `6797825254` and `6805750695`).**
  - **Timeline frame `2635` (`110.04 s`, `src f030`):** Spark peak between knuckle and glass tube rim (`gap_mean_vs_source = 33.4646`, `gap_max_vs_source = 168`).
  - **Timeline frame `2634` (`110.00 s`, `src f029`):** Approved 25% pre-glow (`gap_mean_vs_source = 7.5319`, `gap_max_vs_source = 38`).
  - **Timeline frame `2636` (`110.08 s`, `src f031`):** Approved 50% half-strength decay (`gap_mean_vs_source = 16.2301`, `gap_max_vs_source = 82`).
  - **All other frames (`2560..2633` and `2637..2665`):** No spark anywhere else (`gap_max_vs_source <= 16` across all non-spark take-4 frames `2586..2633` and `2637..2665`).

### Q4. Confirm that no frame of take 4 after its source `f060` appears anywhere in v04
- **CONFIRMED (YES).**
  - Full-frame comparison of `hos_008_master_v04.mp4` frames `2586..2665` against all `192` decoded frames (`f000..f191`) of `02_salon_spark_j2241_t4.mp4` confirms:
    - `2586..2605` map to `f000` (`mad = 1.4967..1.4969`).
    - `2606..2665` map monotonically to `f001..f060` (`mad = 1.5045..1.5964`).
    - Maximum take-4 source frame index used is **`60` (`f060` at timeline frame `2665`)**; minimum MAD against any post-`f060` frame (`f061..f191`) is `2.3408..7.2770`.
  - Timeline frame `2666` cuts cleanly to `03_audience_shock`.
  - All frames outside J2242's 7 verified splice/caption envelopes were verified bitwise-identical to `hos_008_master_v03.mp4` (which predates J2241 take 4), so no post-`f060` frame of take 4 exists anywhere in `hos_008_master_v04.mp4`.
