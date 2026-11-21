# J3287 — Condition Verification Review for J2171 (HOS 009 Shorts A & B Assembly)

- **Verification Job:** `J3287` (`Verify condition for J2171`, `recheck_of: J2171`, `repo: owb`, `kind: review`)
- **Parent Job:** `J2171` (`HOS 009: assemble locked Shorts A/B for conditional 27 and 30 Nov`, `repo: hos`, `film: 009`, `stage: edit`, `after: J0862`, `status: blocked`, `by: gemini`)
- **Verifier:** `gemini` (Mac mini specialist worker; **not** currently elected Chief — `chief_relay.py status` at `2026-11-21T12:20Z` shows **`Chief: Grok Bot`** UP)
- **Checked At:** `2026-11-21T12:12Z`–`2026-11-21T12:20Z`
- **Verdict:** **CONDITION SATISFIED (MET) — RECOMMEND ELECTED HOS CHIEF (`chief` / Grok Bot) REOPEN `J2171` AND CLOSE `J3287`.**
  - Every prerequisite named in `J3230`'s waiting condition on `J2171` (*"Require J3241 formal score acceptance, completed J2035 long assembly with all required gates, and preserved Shorts locked inputs before release"*) AND in `J2171`'s original brief (`J0862` VO disposition, `J2033`/`J2034` picture acceptance, `J2035` long assembly & score bed) is now **DONE** and independently verified on disk and NAS:
    1. **`J3241` formal score acceptance:** `done` (`2026-11-20T17:11Z`, Acting Chief `gemini`). HOS PRs `#698` (`53288fe9`), `#700` (`9b512c8f`), `#701` (`67ed9fb2`), and `#702` (`932fd522`) are merged to HOS `main`. `hos_009_score_v04_synth.wav` (`151ba46acdf7...`) is formally accepted with verified Mini/NAS SHA-256 parity.
    2. **`J2035` long assembly (and `J3261` bounded `£0` v02 re-edit):** Both `done`. Untouched `v01` (`802b5c7e...`) and `v02` (`9d8731cb...`) are directly verified on NAS with `picture_qa` (0/92 fail, 5 warn), `polish_gate` (0/92 fail), `music_gate`, and `sfx_kit level` PASS.
    3. **Preserved Shorts locked inputs & `J2033`/`J2034` picture acceptance (`18/18` rows):** `J0862`/`J2279`/`J2281` Shorts VO (`4/4` MP3+WAV files) match byte-for-byte between Mini and NAS; `J2034` is `done` (`90/90` long rows settled); previously missing Short A `S03` (`P3:07_ball_to_moon`, `07_ball_to_moon_t1.mp4`) is now present and SHA-256 verified across Mini & NAS (`fba484bb...`, `1280×720`, `7.917 s`); all other `17/18` Short A/B rows and `S06` named plate `02_spray_paint_c2_t1.mp4` (`0a6279c0...`) match `INPUT_INVENTORY.json` / `SHORTS_PICTURE_PLAN_v03.json` exactly.
  - **All original gates & Ben-approval boundaries remain intact:** `£0` cash, `0` credits, `ACTIVATION_AUTHORIZED = False`, ElevenLabs ledger untouched since `2026-11-17T16:19:02+00:00`, `J3043`/`J3045` closed unused (`J3047`), `v01`/`v02`/`v03_synth` rejected, `0` duplicate Gravity/Newton/Moon HOS videos in `2026-11-20` snapshot (`69` videos), no YouTube/Studio/Buffer/privacy/upload/schedule changes, `ben_ok` remains `todo`, and no moving-video or audio review claimed from this session.
  - **Why `J3287` is parked for Chief instead of executed directly:** Under `scripts/jobs.py:1059` (`do_reopen`: only the elected Chief may release a verified hold) and `scripts/jobs.py:1561` (`done` on a `recheck_of` job), only the currently elected HOS Chief (`chief` / Grok Bot) may reopen `J2171` and close `J3287`.

---

## 1. Direct Verification Evidence (`2026-11-21T12:12Z`–`12:20Z`)

| Check | Status | Direct Evidence Verified |
|---|---|---|
| **1. `J3241` Formal Score Acceptance & Guardrails** | **SATISFIED** | `J3241` is `done` (`gemini` as Acting Chief, `2026-11-20T17:11Z`). HOS PRs **`#698`** (`53288fe9`, `v03` audit), **`#700`** (`9b512c8f`, `v04_synth` production), **`#701`** (`67ed9fb2`, `J3240` independent `audio_input` ear review `7/7 PASS`), and **`#702`** (`932fd522`, `SCORE_DISPOSITION_v04_synth.{md,json}` + `status.json`) are all `MERGED` on HOS `main`. Directly verified Mini & NAS SHA-256 parity on `05_Music/hos_009_score_v04_synth.wav` = **`151ba46acdf7...`** (`match=True`). Offline guardrails verified intact: `04_Audio/tools/hos009_score_flight.py:34` has literal `ACTIVATION_AUTHORIZED = False`; `~/_desk/elevenlabs/ledger.jsonl` last entry remains `2026-11-17T16:19:02+00:00` (`0` new POSTs, `£0`, `0` credits); `J3043`/`J3045` remain closed unused (`J3047`); `v01`/`v02`/`v03_synth` remain rejected. |
| **2. `J2035` Long Assembly & `J3261` v02 Re-Edit** | **SATISFIED** | `J2035` is `done` and `J3261` is `done` (`£0`). Directly SHA-256 verified both masters on NAS: `09_Assembly/j2035_v01/hos009_long_master_v01.mp4` (`896,216,688` B) = **`802b5c7eb0dd64a77b938e5f26c2f63104c3b851979dabe61e39e70eaf33a833`** (untouched); `09_Assembly/j2035_v02/hos009_long_master_v02.mp4` (`903,809,228` B) = **`9d8731cb49641776027bcbd75a6f4ae5519fc3907c28cb7f422883ebde73ef10`**. Both passed `picture_qa` (`0/92` fail, `5` low-detail warnings), `polish_gate` (`0/92` fail), `music_gate` PASS, and `sfx_kit level` PASS (`v02`: VO `-20.8 LUFS`, SFX `-41.4 LUFS`, `14` hits). Downstream package QA `J2036` (`J3286` verification CONDITION MET on OWB PR `#1105`) and Ben final watch `J2037` remain separate downstream jobs; `J2171` is `£0` assembly prep only and does not upload or schedule before the long is public. |
| **3. `J0862` / `J2279` / `J2281` Locked Shorts VO** | **SATISFIED** | `J0862`, `J2279`, `J2281` are `done` (`HOS PR #423` merged `a7183325`; `status.json` `shorts_vo.state = "done"`). Directly verified exact byte-for-byte Mini & NAS SHA-256 parity on all `4/4` locked VO masters in `10_Shorts/vo_v02/`:<br>• `hos_009_short_A_v02.mp3`: `c2fd407d3aafbe57030b29b213ed128ee4887b785272a2192b4c0809796a1ce6` (`match=True`)<br>• `hos_009_short_A_v02.wav`: `48847b15feda51804a0f6afae1a79aacc74b9bac43ef3eeadda8a7503b745571` (`match=True`)<br>• `hos_009_short_B_v04.mp3`: `0c9c4c6ffdb1337dc11acaf57af909f8d8be91d77210bca2e13af80715b87498` (`match=True`)<br>• `hos_009_short_B_v04.wav`: `a6666fd27c9a90e781369ea07e4888d87a2d5edb1624a0090ae98fa39504686b` (`match=True`) |
| **4. `J2033` / `J2034` Picture Acceptance & All `18/18` Shorts Rows** | **SATISFIED** | `J2034` is `done` (`90/90` HOS 009 picture rows settled). Previously unminted **Short A `S03` (`P3:07_ball_to_moon`)** is now present and directly SHA-256 verified matching across Mini (`hos-009-gravity/.../part03/raw/v05_tranche2/07_ball_to_moon_t1.mp4`) and NAS (`studio-live/.../v05_tranche2_archive/07_ball_to_moon_t1.mp4`) = **`fba484bb8b37055948991f701cf788e8b02015f6e230c866c83f0106e838b95d`** (`1,435,219` B, `1280×720`, `h264`, `7.916667 s`). Directly re-hashed all other `17/18` rows across Short A (`S01`, `S02`, `S04`–`S08`, `loop_tail`) and Short B (`S01`–`S08`, `loop_tail`) plus Short B `S06` named plate `02_spray_paint_c2_t1.mp4` (`0a6279c069fae36a0df291a33d25cce35d0a3aefd4965ebf21ef3e4281bb0f85`): `100%` exact match to `10_Shorts/J2171/INPUT_INVENTORY.json` (`6a0fb1dff2d0...`, Mini==NAS), `READINESS_REPORT.md` (`95bb02af2a91...`, Mini==NAS), and `SHORTS_PICTURE_PLAN_v03.json` (`6a0fb1dff2d0...`, Mini==NAS). |
| **5. Duplicate Check & Live State (`2026-11-20` Snapshot)** | **SATISFIED** | Checked latest HOS analytics snapshot `05_Analytics/hos/snapshots/2026-11-20.json` (`69` videos): **`0`** Gravity/Newton/Moon/Orbit matches. HOS 009 long is not yet uploaded or scheduled; conditional slots (`27`/`30 Nov 11:30 UK`) remain planning targets only, never approval to schedule before the long is public. |

---

## 2. Operational & Rule Notes for `J2171` Once Reopened

To prevent avoidable rework when an assembly worker claims the reopened `J2171`:

1. **VO-locked grandfather clause under Ben's 19 Nov 2026 *Shorts house rules* (`HOS studio/RULES.md:241–263`):**
   - `studio/RULES.md:243` explicitly states: *"VO-locked or scheduled Shorts built to the former 22–27 s band are not reworked unless rule 5 applies."*
   - HOS 009 Short A (`25.32 s`, `hos_009_short_A_v02`) and Short B (`25.48 s`, `hos_009_short_B_v04`) are VO-locked (`J0862`/`J2279`/`J2281`, HOS PR `#423`) and are not a Facebook mirror recut (rule 5). Preserve both locked VO takes untouched (`£0`, zero regeneration) and preserve both `"In one minute"` / `"in one second"` intervals and all `J1004`/`J1894` restrictions.
   - Note: `00_Brand/Channel-Setup/tools/gate_shorts_open.py` now sets `DUR_BAND = (16.0, 19.0)` (warning outside `16–19 s`; `DUR_FAIL = 40.0 s` hard-fail). Record the expected duration WARN honestly under the VO-locked grandfather clause; do not waive any FAIL and do not regenerate VO.
2. **Full-bleed 9:16 hard gate (Ben, 8/10 Nov 2026, `HOS studio/RULES.md:284`):**
   - Every shot in Shorts A and B must fill the full 9:16 frame with zero black bars, flat colour bands, or blurred/mirrored copies above or below (`gate_shorts_open.py` hard-fails padded bands). Reframe 16:9 long plates inside upscale limits and ensure code graphics (`Short_A` `S02`/`S07`, `Short_B` `S04`/`S06` moving-plate composite over `02_spray_paint_c2_t1.mp4`) fill 9:16 cleanly.
3. **Minor NAS text sync (`10_Shorts/SHORTS_SCRIPTS_v02.md`):**
   - Non-blocking drift noted during verification: NAS `studio-live/.../10_Shorts/SHORTS_SCRIPTS_v02.md` (`a79f3aa99e14...`, `24 Oct`) predates the `J2195` Short B opening pickup committed in git `10_Shorts/SHORTS_SCRIPTS_v02.md` (`a37cd406943b...`, `11 Nov`: *"In one minute, the Moon falls five metres. An apple falls that far in one second."*). Git + locked `v04` VO + `SHORTS_PICTURE_PLAN_v03.json` are the source of truth; refresh the NAS text copy during `J2171` assembly.
4. **Score bed & SFX (`£0`):**
   - Reuse accepted `05_Music/hos_009_score_v04_synth.wav` (`151ba46a...`) + synthesised house SFX (`sfx_kit.py make --house hos`), and pass `gate_shorts_open.py check`, `sfx_kit.py level`, `music_gate.py`, and decode/caption/loop checks.
5. **Boundaries:**
   - `£0` / `0` credits. No YouTube upload, scheduling, privacy/retitle, or Buffer writes. Queue the immediate review successor and deliver unique Play links for Ben's final phone watch after Chief review; neither Short airs before the HOS 009 long is public.

---

## 3. Ready-to-Run Action for Elected HOS Chief (`chief` / Grok Bot)

Because `gemini` is a specialist worker while `Grok Bot` (`chief`) is the elected HOS Chief (`scripts/jobs.py:1059, 1561`), `J3287` is parked for `chief` to:

1. **Review & merge this verification record PR** (`jobs/reviews/J3287/REVIEW.md`).
2. **Reopen `J2171` with verification evidence and close `J3287`:**

```bash
python3 scripts/jobs.py reopen J2171 --agent chief \
  --note "J3287 verified CONDITION MET (jobs/reviews/J3287/REVIEW.md): J3241 formally accepted GBP0 score hos_009_score_v04_synth.wav (151ba46a..., HOS PR #698/#700/#701/#702 merged); J2035 v01 (802b5c7e) and J3261 v02 (9d8731cb) long assemblies done with picture_qa/polish_gate/music_gate/sfx_level PASS; J0862/J2281 Shorts VO 4/4 MP3+WAV Mini/NAS parity intact; J2034 done with Short A S03 07_ball_to_moon_t1.mp4 (fba484bb...) and all 18/18 Shorts A/B rows verified; 0 duplicates in 2026-11-20 HOS snapshot; ACTIVATION_AUTHORIZED=False, GBP0. Reopened for GBP0 Shorts A/B assembly (VO-locked grandfather clause under 19 Nov rules; full-bleed 9:16 required; no upload/schedule)." \
  --git

python3 scripts/jobs.py reopen J3287 --agent chief --note "Elected HOS Chief closing completed J3287 verification after reopening J2171" --git
python3 scripts/jobs.py next --agent chief --can mini,any --id J3287 --git
python3 scripts/jobs.py done J3287 --agent chief \
  --result "Elected HOS Chief accepted J3287 CONDITION MET verification (jobs/reviews/J3287/REVIEW.md) and reopened J2171 for HOS 009 GBP0 Shorts A/B assembly." \
  --git
```
