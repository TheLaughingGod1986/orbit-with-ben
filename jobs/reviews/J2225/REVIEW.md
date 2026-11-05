# J2225 — Condition Verification & Native-Video Exact-Source Review for `J1208` (`S5` & `S6` Flow Take 2)

- **Date:** 5 November 2026 (`2026-11-05T16:14Z`)
- **Reviewer / Worker:** `gemini` (`gemini-argon`, demonstrated `audio_input,moving_video_input` registered via `chief_relay.py capabilities`)
- **Verification Task:** `J2225` (`Verify condition for J1208`, `recheck_of: J1208`, `taskKeys: ["OWB:030"]`)
- **Linked Jobs / PR:** `J1208` (`J1204 source follow-up: genuine meteor video and clean Titan opening`), `J2167` (`J1208 exact-source native-video review: S5/S6 Flow take2`), `J1199` (`OWB Shorts airing 3, 7 and 10 Nov: fix frame 0 and the meta-promise`), `PR #507` (`bb22c548ea`, merged to `main` as `542f8c9d44`)
- **Spend:** £0.00 / 0 credits (verification & review only; 40 Flow credits from `15430 -> 15390` already spent in `J1208` and verified in `05_Analytics/ai_spend/ledger.jsonl`; no further Flow or Vertex takes)
- **Source Review Verdict:** **KEEP (Both `S5_flow_t2_silent.mp4` and `S6_flow_t2_silent.mp4` Recommended for Exact-Source Acceptance)**
- **Condition Verification Disposition (`J1208`):** Native-video (`moving_video_input`), phone-copy, forward-preroll continuity, scientific-honesty, and full-size `picture_qa` WARN reviews are **COMPLETE** and **PASS (`KEEP`)**. Because `J1208` requires the current elected Chief (`codex`) to record the final exact-source decision before `J1199` assembly (and `scripts/jobs.py` restricts `reopen` on a held job to the elected Chief), `J1208`'s `capability` hold is updated to an `input` hold via `jobs.py wait J1208 --agent gemini --type input --recheck J2225` referencing this `KEEP` evidence for immediate `J2167` closeout and elected-Chief acceptance.

---

## 1. File Integrity, SHA-256 & Technical Decode Verification (`/Users/benjaminoats/_desk/handoff/J1208/flow-20261105/`)

All candidate files, prospective source windows, phone derivatives, and rejected first takes on the Mac mini match `jobs/reviews/J1208/FLOW_DELIVERY_2026-11-05.md` and `jobs/reviews/J1208/flow-20261105/generation_t2.json`, and decode with `0` `ffmpeg` errors and `0` frozen/repeated frames:

| File | Role / Window | Dimensions & Rate | Frames / Duration | Bytes | SHA-256 | Decode & Step-Diff (`gray`) | Verdict |
|---|---|---|---:|---:|---|---|---|
| `S5_flow_t2_silent.mp4` | **S5 Take 2 native silent master** | `720x1280` @ `24.00 fps` (`1.5x` to `1080x1920`, crop `none`) | `190` (`7.917 s`) | `643,499` | `904868b092ed9b6e93e785805a1179eba7cf9f358f672403fcf5f3826d2e0e18` | `0` err · `min=0.1121`, `med=0.2626`, `max=0.8097`, `zero_steps=0` | **KEEP** |
| `S5_t2_preroll.mp4` | **S5 forward preroll (`0.00–1.15 s`)** | `720x1280` @ `24.00 fps` | `28` (`1.167 s`, `f0..f27`) | `96,792` | `42b63bcea6e9c4ac98a68b2f6fd8c12fa31834534594a0999653a13a581bf235` | `0` err · `min=0.1225`, `med=0.2577`, `max=0.5323`, `zero_steps=0` | **KEEP** |
| `S5_t2_opening.mp4` | **S5 opening (`1.15–3.85 s`)** | `720x1280` @ `24.00 fps` | `65` (`2.708 s`, `f28..f92`) | `228,294` | `996db1505f3283b78e5cf7935668adca44e03e0fc04c507e95276590caa19faf` | `0` err · `min=0.1416`, `med=0.2808`, `max=0.5264`, `zero_steps=0` | **KEEP** |
| `S5_t2_phone_source.mp4` | **S5 phone proxy (`0.00–3.85 s`)** | `360x640` @ `24.00 fps` | `93` (`3.875 s`) | `67,148` | `93ddd4ae6e9f38394259bf3397937d196462c763d596765faec9a4cc796b8aea` | `0` err · `min=0.0927`, `med=0.2279`, `max=0.5575`, `zero_steps=0` | **KEEP** |
| `S6_flow_t2_silent.mp4` | **S6 Take 2 native silent master** | `720x1280` @ `24.00 fps` (`1.5x` to `1080x1920`, crop `none`) | `190` (`7.917 s`) | `2,275,883` | `2218c817e96a1444da45a7130e5cc8d0cc8824a322f4a16ed6078c85562dad2a` | `0` err · `min=3.3146`, `med=4.2048`, `max=5.0941`, `zero_steps=0` | **KEEP** |
| `S6_t2_preroll.mp4` | **S6 forward preroll (`0.00–1.15 s`)** | `720x1280` @ `24.00 fps` | `28` (`1.167 s`, `f0..f27`) | `204,010` | `ae878ffea0a00b397c8b4286c69204dda77326abb895d15dfc33147f6fdcff51` | `0` err · `min=3.2761`, `med=4.1645`, `max=4.8235`, `zero_steps=0` | **KEEP** |
| `S6_t2_opening.mp4` | **S6 opening (`1.15–3.85 s`)** | `720x1280` @ `24.00 fps` | `65` (`2.708 s`, `f28..f92`) | `500,620` | `1356d8e933b048dac9e5996832b8de87af8a6d2179591928f02a98ce7c13936e` | `0` err · `min=3.3289`, `med=3.9491`, `max=5.0371`, `zero_steps=0` | **KEEP** |
| `S6_t2_phone_source.mp4` | **S6 phone proxy (`0.00–3.85 s`)** | `360x640` @ `24.00 fps` | `93` (`3.875 s`) | `182,801` | `6b13d66e7dfbd32d4fd26e92c2fcac1bd1fc7c8aaecba66e8c10e0890634de66` | `0` err · `min=2.6475`, `med=3.4546`, `max=4.3902`, `zero_steps=0` | **KEEP** |
| `S5_flow_t1_silent.mp4` | Rejected S5 Take 1 | `720x1280` @ `24.00 fps` | `190` (`7.917 s`) | `2,145,108` | `434a9e1dbbb87298eb87760fe0d9bf55708a92eeea54e449b0fb22b231806389` | Near-black FAIL at `2.50 s` (`mean 24.91`) + head exits early | **FIX (Excluded)** |
| `S6_flow_t1_silent.mp4` | Rejected S6 Take 1 | `720x1280` @ `24.00 fps` | `190` (`7.917 s`) | `3,534,566` | `624b87eeabcb9657d503c73da43f226b8649f59644f3d3ab78e84ca07a269719` | Unapproved giant celestial disc in sky | **FIX (Excluded)** |

---

## 2. Direct Native-Video (`moving_video_input`), Phone, Preroll & Full-Size WARN Review

Both `S5_flow_t2_silent.mp4` and `S6_flow_t2_silent.mp4`, their split `opening` (`1.15–3.85 s`) and `preroll` (`0.00–1.15 s`) clips, their `360x640` phone proxies (`S5_t2_phone_source.mp4`, `S6_t2_phone_source.mp4`), their 16-panel contact sheets (`S5_t2_sheet.jpg`, `S6_t2_sheet.jpg`), their full-size frame extracts (`t=0.000s, 0.575s, 1.150s, 2.500s, 3.800s`), and their full-size `picture_qa_review.jpg` sheets were directly inspected via multimodal `read_file`:

### A. `S5` (*What Are Shooting Stars Really Made Of?* · `T9fVlG3CCzU` · Locked line 1: *"That shooting star isn't a star."*)
1. **Subject Recognition & Frame-0 Motion (`1.15–3.85 s`, `65` frames):**
   - At `t = 1.150 s` (frame `28`, output frame 0 of the `2.70 s` opening window), a bright white-blue meteor head with a crisp luminous ionized wake is immediately recognizable in the upper-left/central sky and already moving diagonally downward-right across a well-exposed purple-to-amber twilight gradient (`luma_mean = 64.59–78.33`, zero near-black frames).
   - Across `1.15–3.85 s`, the meteor travels steadily and continuously through the central third of the vertical 9:16 frame (`MAD_opening_first_to_1_5s = 5.9322` RGB / `6.0073` gray; `zero_steps = 0`), with the bright meteor head remaining well inside the frame through `t = 3.850 s`.
   - In `S5_t2_phone_source.mp4` (`360x640`), the glowing meteor head and wake read immediately at mobile scale from frame 0, sitting cleanly in the upper-middle sky with ample headroom for the top hook caption and bottom subtitles.
2. **Forward Preroll (`0.00–1.15 s`, `28` frames) & Loop Continuity:**
   - The forward preroll (`0.00–1.15 s`, frames `0..27`) shows the exact same meteor entering upper-left and advancing smoothly along the identical trajectory into frame `28` (`t = 1.150 s`).
   - The boundary step at `f27 -> f28` (`1.15 s`) has `MAD = 0.2503` (matching the clip's `0.2626` median frame step), guaranteeing a contiguous, jump-free forward loop from the end of the Short's 1-second loop tail back to opening frame 0.
3. **Scientific Honesty & Creative Brief (`SCRIPTS_v01.md` / `GEMINI_FACTS_S5-S8_v01.md`):**
   - Visually depicts a single bright atmospheric meteor streak above a low, unobtrusive dark horizon silhouette with faint background stars. Contains no constellation lines, labels, telescope reticle, exploding star, macro fireball/impact plume, UI, watermarks, or Orbit character. Properly classified as a generated explanatory illustration requiring description disclosure (no fake NASA credit; no corner credit on the Short).
4. **Full-Size `picture_qa_review.jpg` WARNs (`S5_t2_source_qa/picture_qa_review.jpg`):**
   - `0:01 row preroll`: `illustration` (`Generated explanatory S5 illustration; Flow Veo 3.1 Fast; not observational footage`) + `low detail: edge density 0.0054 < film p5 0.0055`. Full-size inspection confirms the low edge-density metric simply reflects the smooth natural twilight sky gradient surrounding the crisp meteor streak, with no compression blockiness or banding -> **KEEP**.
   - `0:02 row opening`: `illustration` (`Generated explanatory S5 illustration; Flow Veo 3.1 Fast; not observational footage`). Full-size inspection confirms sharp meteor head, clean wake, and natural sky gradient -> **KEEP**.

### B. `S6` (*What Would Standing on Saturn's Moon Titan Feel Like?* · `RLSJm59OSzI` · Locked line 1: *"Standing on Titan feels like being fifteen metres underwater."*)
1. **Subject Recognition & Frame-0 Motion (`1.15–3.85 s`, `65` frames):**
   - At `t = 1.150 s` (frame `28`, output frame 0 of the `2.70 s` opening window), the shot presents a wide eye-level view across low-relief, gently undulating brownish-orange Titan terrain beneath a thick, muted amber-orange atmospheric haze with softly drifting cloud/haze layers.
   - Across `1.15–3.85 s`, the eye-level perspective advances smoothly over the textured terrain while the orange atmospheric haze drifts visibly (`MAD_opening_first_to_1_5s = 13.7192` RGB / `14.5679` gray; `step_diff min=3.3289, med=3.9491, max=5.0371`, `zero_steps = 0`; `luma_mean = 125.42–133.84`).
   - In `S6_t2_phone_source.mp4` (`360x640`), the murky orange Titan atmosphere and low-relief surface read clearly at phone scale from frame 0, with clean upper-sky space for the hook caption and lower-third contrast for subtitles.
2. **Forward Preroll (`0.00–1.15 s`, `28` frames) & Loop Continuity:**
   - The forward preroll (`0.00–1.15 s`, frames `0..27`) carries the same smooth forward eye-level motion and drifting orange haze directly into frame `28` (`t = 1.150 s`).
   - The boundary step at `f27 -> f28` (`1.15 s`) has `MAD = 5.0421` (within the clip's natural `3.31–5.09` frame-to-frame motion range), providing a continuous forward loop handoff into opening frame 0.
3. **Scientific Honesty & Creative Brief (`SCRIPTS_v01.md` / `GEMINI_FACTS_S5-S8_v01.md`):**
   - Completely eliminates Take 1's giant celestial disc in the sky: the upper sky is entirely opaque, diffuse orange nitrogen/methane haze informed by Huygens optical descent/surface appearance. Contains no Saturn, no rings, no sun/moon disc, no dramatic invented mountains, no Earth-blue sky, no underwater scene, no radar swath artifacts, and no fabricated geometry. Does not claim to reconstruct a measured landing site and does not equate visual haze with the spoken numerical pressure comparison. Properly classified as a generated explanatory illustration requiring description disclosure.
4. **Full-Size `picture_qa_review.jpg` WARNs (`S6_t2_source_qa/picture_qa_review.jpg`):**
   - `0:01 row preroll`: `illustration` (`Generated explanatory S6 illustration; Flow Veo 3.1 Fast; not observational footage`). Full-size inspection confirms clean terrain texture and diffuse amber haze -> **KEEP**.
   - `0:02 row opening`: `illustration` (`Generated explanatory S6 illustration; Flow Veo 3.1 Fast; not observational footage`) + `low detail: edge density 0.0704 < film p5 0.0707`. Full-size inspection confirms the edge-density WARN is caused by the physically appropriate diffuse orange atmospheric haze filling the upper sky above sharp foreground terrain ripples -> **KEEP**.

---

## 3. Exact-Source Recommendation & `J1208` Condition Disposition

1. **Exact-Source Recommendation (`KEEP` for Elected-Chief Acceptance & `J1199` Assembly):**
   - **`S5` (*What Are Shooting Stars Really Made Of?*):** Accept `/Users/benjaminoats/_desk/handoff/J1208/flow-20261105/S5_flow_t2_silent.mp4` (`sha256: 904868b092ed9b6e93e785805a1179eba7cf9f358f672403fcf5f3826d2e0e18`), `720x1280` @ `24 fps` upscaled `1.5x` to `1080x1920` (crop `none`, speed `1`), **opening window `1.15–3.85 s` (`2.70 s`)**, **forward loop preroll `0.00–1.15 s` (`1.15 s`)**, with generated-illustration description disclosure.
   - **`S6` (*What Would Standing on Saturn's Moon Titan Feel Like?*):** Accept `/Users/benjaminoats/_desk/handoff/J1208/flow-20261105/S6_flow_t2_silent.mp4` (`sha256: 2218c817e96a1444da45a7130e5cc8d0cc8824a322f4a16ed6078c85562dad2a`), `720x1280` @ `24 fps` upscaled `1.5x` to `1080x1920` (crop `none`, speed `1`), **opening window `1.15–3.85 s` (`2.70 s`)**, **forward loop preroll `0.00–1.15 s` (`1.15 s`)**, with generated-illustration description disclosure.
   - **Excluded First Takes:** `S5_flow_t1_silent.mp4` (`434a9e1d...`) and `S6_flow_t1_silent.mp4` (`624b87ee...`) remain **FIX / Excluded** and must never be used.
2. **Condition Update on `J1208` (`wait --recheck J2225`):**
   - The `moving_video_input` capability requirement on `J1208` is now satisfied by this review (`jobs/reviews/J2225/REVIEW.md`), and `PR #507` (`bb22c548ea`) is merged on `main` (`542f8c9d44`).
   - Because `J1208` requires the current elected Chief (`codex`) to record the final exact-source decision before `J1199` assembly (and `scripts/jobs.py` restricts `reopen` on a held job to the elected Chief), `J1208` is updated with `jobs.py wait J1208 --agent gemini --type input --recheck J2225` so `J2167` / elected Chief can immediately adopt this `KEEP` review and unblock `J1208` / `J1199` assembly.
   - All existing cuts, manifests, VO stems, YouTube schedules, Buffer state, and scheduled-copy fallbacks remain untouched.
