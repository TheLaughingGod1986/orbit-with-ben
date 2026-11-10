# J2356 Condition Verification Review — J2320 (`034 Pluto Short 2 (Keeper question): build 22-27s Charon/water-ice cut + gates`)

- **Job**: `J2356` (`Verify condition for J2320`)
- **Parent Job**: `J2320` (`034 Pluto Short 2 (Keeper question): build 22-27s Charon/water-ice cut + gates (slot Wed 23 Dec 11:30 London; no upload)`, `film: 034`, `stage: edit`, `repo: owb`, `progress: 1/3`, `after: J2157`, `due: 2026-12-23T10:30:00Z`)
- **Upstream & Related Jobs**:
  - `J2223` (`Shorts slots for the Wed 9 Dec and Sun 13 Dec longs (Uranus, Pluto): two Shorts each`, `status: done` by `macbook`, queued `J2320` with `after: J2157`)
  - `J2157` (`034 Pluto: VO from locked script v03`, `status: done`, accepted in `J2352`)
  - `J2352` (`034 Pluto: elected Chief rules on reconciled J2157 v03 evidence (PR #619) and full VO PASS`, `status: done` by `codex` at `2026-11-07T08:20Z`, `jobs/reviews/J2352/REVIEW.md`)
  - `J2353` (`034 Pluto: shot list from approved v03 VO`, `film: 034`, `stage: shots`, `after: J2352`, `status: open`, `for: gemini`)
  - `J2319` / `J2354` (`034 Pluto Short 1` and its companion verification review `jobs/reviews/J2354/REVIEW.md`, `fc5e4f0df2`)
- **Reviewer**: `gemini` (`gemini-argon`, 7 November 2026)
- **Verdict**: **CONDITION NOT YET SATISFIED (`HOLD — AWAITING J2353 SHOT LIST, SHORTS_PLAN_v01.md, DELIVERED CHARON/WATER-ICE PICTURE & CODE GRAPHICS, AND HOUSE MUSIC/SFX`) — Keep `J2320` blocked at step `1/3` (`--type dependency --recheck J2356`, preserving original retry `2026-11-08T08:30:00Z`). While `034` VO `v03` (`2be8030b6c42b673530351014c71bca1a6c31a10af9746539bb2a1ce7dcf7685`) and script `v03` (`f9852589a7ea9888165c5148c9d60196cb174d7a41104ad442d845f2dbde65cc`) are locked and approved (`J2352`), `J2353` (`034 Pluto: shot list from approved v03 VO`) remains `open` and explicitly forbids assembly until the shot list is reviewed, and none of the required Short 2 inputs (`10_Shorts/SHORTS_PLAN_v01.md`, `03_Picture/`, `05_Music/`, `06_Sound-Effects/`, Charon or water-ice motion plates, or code graphics) exist on disk yet.**

---

## 1. Recorded Waiting Condition on `J2320`

`J2320` was blocked at `2026-11-07T08:53Z` (`by: codex`, `hold.type = "dependency"`, original `check_at = "2026-11-08T08:30:00Z"`, `recheck_task = "J2356"`) with:
> `J2353 shot list must be reviewed before assembly (its explicit restriction). Referenced 034/10_Shorts/SHORTS_PLAN_v01.md, 03_Picture, 05_Music and 06_Sound-Effects are absent on disk at 2026-11-07T08:55Z; no reusable Charon motion or house music delivered. Brief quoted Charon lift is not verbatim approved v03 STT: actual text includes In mutual tidal locking ... Charon neither rises nor sets at 236.10-244.70s. Resume from approved v03 only once reviewed Short wording/lift and actual picture/music inputs exist; preserve 22-27s, question-first and all gates. No upload or new paid generation authorised.`

*(Note on why `J2356` was queued immediately at `08:53Z`: `J2320` has `after: "J2157"` (`done`) and `hold.type == "dependency"` with no `last_recheck` recorded yet; in `scripts/workflow_state.py` lines 110–112, a dependency hold with `after` done and `not hold.get("last_recheck")` immediately triggers one initial verification task. Recording `--recheck J2356` sets `last_recheck: "J2356"`, after which `hold_due` honours `check_at`.)*

---

## 2. Direct Verification Evidence (`2026-11-07T08:57Z`)

1. **Approved Voice-Over & Script Master on Disk — SATISFIED (`VO ONLY`):**
   - `01_Script/pluto_frozen_heart_script_master_v03.md`: `f9852589a7ea9888165c5148c9d60196cb174d7a41104ad442d845f2dbde65cc`
   - `02_Voiceover/pluto_frozen_heart_vo_v03.wav`: `2be8030b6c42b673530351014c71bca1a6c31a10af9746539bb2a1ce7dcf7685` (`616.160 s`, accepted in `J2352` / `jobs/reviews/J2352/REVIEW.md`)
   - `02_Voiceover/pluto_frozen_heart_vo_v03.mp3`: `86cfc44247d0c8e7aee535c2fe50edb5038351041008e3f304e82fd84f124456`
   - `02_Voiceover/pluto_frozen_heart_vo_v03_TAKE.json`: `370b876904c53040f4b40a5c34aa838caef005d2c97b24edeb0c1c268ae5deb6`
   - `02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_raw.json`: `af85f3b6fbcb4c0f549f19f0c526fed18f9454bdb9cfa27958ff5a2770d75df7`
   - `02_Voiceover/stt/pluto_frozen_heart_vo_v03/words.srt`: `cd4168acc18022c764a13c501c576ad3d84a72f3b1e0944a23ee68a6d79d51b3`

2. **Shot List & Upstream Gate (`J2353`) — UNMET:**
   - `J2353` (`034 Pluto: shot list from approved v03 VO`, `film: 034`, `stage: shots`, `after: J2352`) is currently **`open`** (`created_at: 2026-11-07T08:19Z`).
   - `J2353`'s brief explicitly mandates: *"Zero-spend planning only; no generation or assembly until the shot list is reviewed."*
   - `02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/status.json` has only `topic`, `script`, `sources`, and `vo` marked `done`, with `shots` and `picture` not yet started.

3. **Required Short 2 Plan, Picture, Music, and SFX Inputs on Disk — UNMET:**
   - `10_Shorts/SHORTS_PLAN_v01.md`: **ABSENT** (`10_Shorts/` contains only `README.md`, `251` bytes).
   - `03_Picture/`, `05_Music/`, `06_Sound-Effects/`, `09_Rough-Cut/`: **ABSENT** (directories do not exist in `02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/`).
   - `04_Generated-Clips/`: contains only `01_Raw/.gitkeep` (`0` media files; `0` `.mp4` files anywhere in the `034` film folder).
   - Neither New Horizons Charon/Pluto plates (`PIA19968` / `PIA19966`), nor the `1,214 km` / `19,640 km` / `153-hour` Charon code graphics, nor the `2–3 km` water-ice mountain plates/cutaway graphic, nor the `034` house music bed and SFX kit have been delivered yet.

4. **Verbatim `v03` STT Transcript Reconciliation (`J2320` Brief vs Locked `v03` VO):**
   - `J2320` was drafted at `2026-11-07T00:07Z` before `J2352` finalised `pluto_frozen_heart_vo_v03.wav`, quoting unrecorded prose (*"Why does Pluto's largest moon hang frozen in one spot in the sky? Discovered in 1978, Charon is about twelve hundred kilometers across..."*).
   - In the approved `pluto_frozen_heart_vo_v03.wav` (`stt_raw.json` / `words.srt`), the exact recorded sentences for the two candidate Short 2 lifts are:
     - **Option A — Ch 1→Ch 2 Charon Double-World / Mutual Tidal Lock Lift (`stt_raw.json`):**
       - `152.460–158.620 s` (`6.160 s`, `13` words, literal spoken question): *"Why did a secret 19,000 kilometers away turn Pluto into a double world?"*
       - `192.900–206.700 s` (`13.800 s`, `30` words): *"At 1,214 kilometers across, Charon is about half the size of Pluto, the largest known satellite relative to its parent body in our solar system, often called a double planet."*
       - `207.960–212.720 s` (`4.760 s`, `6` words): *"Charon orbits Pluto at 19,640 kilometers."*
       - `213.380–217.200 s` (`3.820 s`, `10` words): *"By comparison, our moon is 20 times farther from Earth."*
       - `236.100–248.460 s` (`12.360 s`, `29` words; `"Charon neither rises nor sets"` at `242.740–244.700 s`): *"In mutual tidal locking, the same surfaces of Charon and Pluto always face each other, so Charon neither rises nor sets, hovering over the same spot on Pluto's surface."*
       - *(Combining the `152.460–158.620 s` question + `192.900–206.700 s` scale + `236.100–248.460 s` tidal-lock payoff = `72` words / `32.32 s` raw; or `152.460–158.620 s` + `207.960–217.200 s` + `236.100–248.460 s` = `58` words / `27.10 s` raw, `~25.5–26.5 s` with clean inter-sentence pause trims, inside the `22–27 s` / `55–65 w` Keeper window.)*
     - **Option B — Ch 4→Ch 5 Water-Ice Mountains Lift (`stt_raw.json`, `J2320` §Alternate):**
       - `441.760–451.060 s` (`9.300 s`, `15` words, literal spoken question): *"Why can towering mountains stand beside a flowing glacier between -226 and -240 degrees Celsius?"*
       - `455.100–460.660 s` (`5.560 s`, `18` words): *"On Earth, water ice is a soft glacier that melts, and rock is the solid ground beneath it."*
       - `461.380–473.040 s` (`11.660 s`, `18` words): *"At -226 to -240 degrees Celsius, over 200 degrees below water's zero-degree freezing point, water is essentially rock-like."*
       - `474.000–481.620 s` (`7.620 s`, `18` words): *"Pluto's two to three-kilometer mountains are big blocks of water ice, sometimes coated with frozen gases like methane."*
       - *(Combining the `441.760–451.060 s` question + `461.380–473.040 s` physics + `474.000–481.620 s` payoff = `51` words / `28.58 s` raw, or `~25.5–26.5 s` with natural pause trims between sentences.)*
   - `SHORTS_PLAN_v01.md` and `J2353`'s shot-list review must lock the exact verbatim `v03` sentence selection before `J2320` cuts audio or picture.

---

## 3. Queue Action & Protected Elected-Chief Handoff

- Because `scripts/jobs.py` (`set_wait` line 354) restricts `jobs.py wait J2320 --recheck J2356` to the elected Chief (`Only the elected Chief may record a condition check`, currently `Chief: Codex`), `J2356` is parked for Chief with complete verification evidence in this document.
- Elected Chief (`codex`) can record the condition check on `J2320` and close `J2356` with:
  ```bash
  python3 scripts/jobs.py wait J2320 --agent codex --type dependency --recheck J2356 \
    --condition "J2356 condition check (jobs/reviews/J2356/REVIEW.md): 034 VO v03 (2be8030b6c42b673530351014c71bca1a6c31a10af9746539bb2a1ce7dcf7685) and script v03 (f9852589a7ea9888165c5148c9d60196cb174d7a41104ad442d845f2dbde65cc) are locked and approved (J2352), but J2353 (034 shot list from v03 VO) remains open and forbids assembly until reviewed, and 10_Shorts/SHORTS_PLAN_v01.md, 03_Picture, 05_Music, 06_Sound-Effects, Charon/water-ice plates, and code graphics are still absent on disk. Resume only once J2353 is reviewed, SHORTS_PLAN_v01.md locks the verbatim v03 STT lift, and picture/music inputs are on disk." \
    --check-at "2026-11-08T08:30:00Z" \
    --action "Await reviewed Pluto shot list (J2353), verbatim v03 Short 2 lift plan, and delivered Charon/water-ice picture and music before build" --git
  python3 scripts/jobs.py done J2356 --agent codex --ref jobs/reviews/J2356/REVIEW.md \
    --result "HOLD / CONDITION UNMET (jobs/reviews/J2356/REVIEW.md): Verified 034 on disk at 2026-11-07T08:57Z. VO v03 (2be8030b6c) and script v03 (f9852589a7) are locked and approved (J2352), but J2353 shot list remains open and 10_Shorts/SHORTS_PLAN_v01.md, 03_Picture, 05_Music, 06_Sound-Effects, and Charon/water-ice picture/music inputs are absent on disk. Exact v03 STT timestamps for Charon and water-ice lifts documented. J2320 kept blocked at 1/3 (--recheck J2356, next check 2026-11-08T08:30:00Z)." --git
  ```
