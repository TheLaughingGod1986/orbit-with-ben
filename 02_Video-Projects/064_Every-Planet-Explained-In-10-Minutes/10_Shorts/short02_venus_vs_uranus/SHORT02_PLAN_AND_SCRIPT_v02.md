# OWB:064 Short 2 — Plan v02: J3912 fixes, shot provenance and duration (`SHORT02_PLAN_AND_SCRIPT_v02.md`)

- **Job:** J3913 (writer: `claudecode`, covering for Claude). Parent J3904 stays held. Chief ruling J3912 = FIX (review commit `42e48a4d90`).
- **Supersedes:** the v01 plan's checklists and "PASS" claims. v01 files are kept unchanged for history.
- **Spend:** £0. No ElevenLabs, Flow or Vertex. No media generated, no upload, no schedule change. **Nothing is locked.**
- **Script:** `064_short02_venus_vs_uranus_script_v02.md` (primary v02 plus a 16–19 s variant v02b). **Claims:** `064_short02_CLAIMS_v02.md`.

## 1. Fix 1: surface vs atmosphere, and the winter sentence
Covered in the script file. Line 1 says Venus's surface and Uranus's air. Line 2 calls −224 the atmosphere's minimum and keeps "in some places". The v01 winter clause is removed because, next to the minimum, it read as an unsupported cause.

## 2. Fix 2: Gemini claim and quote check
`064_short02_CLAIMS_v02.md` holds 9 rows with direct URLs and the exact quotes expected. **It has not been run.** The check belongs before lock, under the dependent review; every flag gets resolved in `064_short02_QUOTECHECK_v02.md`.

## 3. Fix 5: duration rule, cited
- **J3904 brief (27 Nov 2026, explicit):** "Must follow all existing Shorts gates (22-27 s, …)".
- **`studio/RULES.md` line 189:** "the Shorts duration gate warns outside 16.0–19.0 s (Ben, 19 Nov 2026); ≥ 40 s still hard-fails".
- **`00_Brand/Channel-Setup/tools/gate_shorts_open.py` lines 113–114:** "# Ben, 19 Nov 2026 (Shorts house rules, PR #676): new masters target 16.0–19.0 s, both edges inclusive." `DUR_BAND = (16.0, 19.0)`; a duration outside the band is a **warn**, not a fail; `DUR_FAIL = 40.0`.
- **`FAMILIAR_DANGER_STRATEGY.md` line 122** says the same (warns outside 16.0–19.0 s, hard-fails at 40 s).
- **Older lines still say 22–27 s** (for example `studio/RULES.md` lines 67, 86, 288: "every other Short stays 22–27 s and 55–65 words").

**Reading:** Ben's 19 Nov rule is the newer one. A 22–27 s master gets a gate **warn**, not a fail. The J3904 brief asks for 22–27 s explicitly. As the J3912 ruling says, **v02 keeps the brief's 22–27 s** until a reviewer records the resolution, and **v02b** is drafted so that reviewer can pick 16–19 s without another writing round. Writer's recommendation: **v02b** (the newer rule from Ben, and no gate warn). The reviewer decides. The rule texts don't agree with each other; resolving that is for the Chief, not this job.

Recomputed metrics are in the script file. In short: v02 is 284 raw characters, 60 expanded words, about 25.4 / 27.3 / 28.9 s (fast/mid/slow), payoff about 87% in. v02b is 200 raw characters, 40 expanded words, about 17.0 / 18.2 / 19.3 s, payoff about 82% in. All of these are estimates.

## 4. Fix 4: shot provenance and licence (checked on the NAS on 27 Nov 2026; nothing watched)
**The v01 shot list misdescribed three of its nine shots.**

| Cut | v01 said | What the files show | Class | Licence/credit status |
|---|---|---|---|---|
| R01 | "Real moving Parker Solar Probe WISPR" `023/.../harvest_v04/svs14095_WISPR_4thflyby.mp4` | **Not found** at the v01 path: `studio-live/.../023_What-Happened-To-Venus/` holds only `02_Voiceover`, `05_Music`, `08_Thumbnail`. A 40 s search of `mac-mini-archive` found nothing. | Expected: an observational image sequence (native motion) if the NASA SVS 14095 file is found | **Unverified.** Find the file, check its SHA (`11aa1171…`), and read the SVS 14095 page for its credit (NASA/JHUAPL/NRL) and terms. |
| R02 | "Real moving SDO AIA 171 Venus transit" | **Not found** at the v01 path (same reason as R01) | Expected: an observational time-lapse | **Unverified.** NASA SDO media are usually free to use with credit; confirm on the source page. |
| R03 | "Real moving **Keck II** Uranus cloud deck" `033/.../J2334_fix/r55_cut1_r55b_100x_silent.mp4` | Built by `J2334_fix/build_r55.py` from `033/.../J2332/r55b_flow_t1_silent.mp4`. Per `J2332/generation.json` that clip is **Flow Veo 3.1 Fast text-to-video**: "CGI illustration. Not observational footage." … "NOT KEEP." | **AI-generated CGI. Not real footage, not Keck.** | Our own generation. It must be labelled CGI, it can't be called NASA or Keck, and it was never kept. |
| R05 | "Real moving Voyager 2 PIA01488" `r55_cut3_pia01488_pushin_silent.mp4` | `build_r55.py` cut 3: the PIA01488 **still** (2118×2618), colour-graded "blue-green haze deck on #050814 navy space with fine grain and smooth slow camera push-in". | **Still-derived push-in on a graded still. Not native motion.** | NASA/JPL Voyager 2 imagery: public domain with credit; confirm on the PIA01488 page. The grade and grain are our edit. |
| R06 | "Real moving **Keck II** Uranus vortex" `r55_cut2_r55b_128x_vortex_silent.mp4` | Same Veo 3.1 Fast source as R03 (frames 95–189, cropped 1.28×, then **1.92× upscale**) | **AI-generated CGI. Not real footage, not Keck.** | As for R03. |
| R04 | JWST `weic2332a_hires.jpg` | A still (v01 said so) | Still push | ESA/Webb images are **CC BY 4.0** (credit NASA, ESA, CSA, STScI and the named processor). That means attribution is required; they are **not public domain**. Confirm the exact credit line on esawebb.org/images/weic2332a. |
| R07 | Magellan `PIA00215.jpg` | A still | Still push | NASA/JPL: public domain with credit; confirm on the PIA page. |
| R08 | "Real moving WISPR + Magellan" `svs14095_WISPR_Magellan_4thFlyby.mp4` | **Not found** at the v01 path | Unverified (it may be a composite or animation: check the SVS 14095 page) | **Unverified.** |
| R09 | `PIA23791.jpg` / `pvo_uv_790205.jpg` | Stills | Still push | PIA23791 is credited JAXA/ISAS/DARTS/Kevin M. Gill. **Don't treat it as NASA public domain**; check the terms on its page before use. PVO: NASA, public domain with credit; the v01 `023` path was not found. |

**What this means for the plan:**
- The v01 "frame 0 is real moving NASA footage" claim rests on R01, a file **not found** at its stated path. It still needs native moving subject footage at frame 0. The assembler must find and verify that file, or a replacement, before building.
- **R03 and R06 must be dropped or relabelled as CGI.** The Uranus beats have **no native moving Uranus footage** at all right now. Candidates for the next shot plan: a real NASA/ESA image sequence of Uranus if one exists on the shelf, or honest still pushes (JWST weic2332a, Voyager PIA01488) labelled as still-derived. The description's credits must drop "W. M. Keck Observatory".
- The draft manifest's "Pictures:" and "Image credits:" lines are wrong in the same ways. The listing job rewrites them after lock.
- No motion or audio was reviewed. This is a file and metadata audit only.

## 5. Fix 3: retention and "PASS" claims withdrawn
Everything v01 marked `[x]` or "100% PASS" (Keeper, first second, cut timing, ≥70% payoff, seam, 60% stayed-to-watch, 70% viewed, loop, full-bleed) is now a **target or estimate, with checks pending on files that don't exist yet**. There is no take and no render. Runtime, word onsets, payoff timing, loop seam, upscale and the media gates (`gate_shorts_open.py`, `picture_qa.py`, `polish_gate.py`, `music_gate.py`, `sfx_kit.py level`) can only be measured on the eventual files. Audience retention cannot be certified before a Short exists. The v01 §6 slot suggestion (Wed 30 Dec 11:30) stays a suggestion only; the schedule isn't touched.

## 6. For the dependent reviewer (J3914)
1. Choose v02 (22–27 s brief) or v02b (16–19 s rule), and record why.
2. Run the Gemini check on `064_short02_CLAIMS_v02.md` and resolve every flag in `064_short02_QUOTECHECK_v02.md`.
3. Re-plan the Uranus shots without the Veo clips (or with them labelled CGI, if the Chief allows that), and locate the R01/R02/R08 files or replace them.
4. Only then: script lock, and a separate bounded VO decision (live balance, existing credit holds, approved voice). No cash, top-up or overage.
