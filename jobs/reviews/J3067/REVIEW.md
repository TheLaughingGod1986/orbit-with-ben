# J3067 Condition Verification Review — J2993 (`WW2 pilot 001: picture, maps, edit and thumbnail, to Ben's watch`)

- **Verification Job:** `J3067` (`Verify condition for J2993`, `recheck_of: J2993`, `repo: owb`)
- **Parent Job:** `J2993` (`WW2 pilot 001: picture, maps, edit and thumbnail, to Ben's watch`, `status: blocked`, `by: codex`, `needs: mini`, `kind: assembly`, `after: J2992`, `film: WW2:001`, `stage: edit`, `due: 2026-11-25T18:00:00Z`)
- **Verifier:** `gemini` (`Gemini 4 Argon (High)`, specialist worker on the Mac mini via fallback chain on `--kind review` while `claude` is out of usage until `2026-11-18T21:50:00Z`; `Grok Bot` [`chief`] is currently elected Chief)
- **Demonstrated Media Capability:** Recorded `chief_relay.py capabilities --agent gemini --available ''` at session start (`J3067` is a queue condition verification task; no audio audition or moving-video perception is claimed in this session).
- **Checked At:** `2026-11-18T18:53Z`
- **Verdict:** **PREDECESSOR `J2992` COMPLETE ON DISK, BUT `J2993` REMAINS BLOCKED ON AN EXPLICIT CHIEF SCOPE RULING & UNMERGED PREDECESSOR PRs (`J2993` was parked by `codex` at `2026-11-18T18:31Z` [`a273ddc4b3`, PR `#1012` @ `820c156807`] asking the Chief to scope archive fallback/code-illustration rules for the 34 archive narration windows after `iwm.org.uk` HTTP 403 and NHHC direct-page 404/timeout failures; additionally, predecessor PRs `#996`/`ww2-channel#4` [`J2991` script/sources/claims check] and `#998`/`ww2-channel#2` [`J2992` narration] remain `OPEN` and unmerged; `£0.00` cash / `0` credits spent).**

---

## 1. Recorded Waiting Condition, Block Reason & Remaining Action

- **`J2993["hold"]["condition"]` (auto-attached by `reconcile_holds` in `6323c4401d` because `J2993` has `"after": "J2992"`):**
  ```text
  Required predecessor is complete; verify remaining gates and approvals
  ```
- **`J2993["result"]` (actual block reason recorded by `codex` at `2026-11-18T18:31Z` in `a273ddc4b3`):**
  ```text
  parked for Chief: repeated IWM/Navy archive routes exhausted; choose a bounded new source approach or accurate sourced code illustrations for uncleared windows. Timing work committed at 820c156807; read J2993_CONTINUATION_v06.md. Full edit and score still unfinished; no Ben watch submission.
  ```
- **`J2993["remaining_action"]`:**
  ```text
  Choose archive replacements, then finish the full edit and score
  ```

---

## 2. Element-by-Element Gate & Evidence Verification on the Mac mini (`2026-11-18T18:53Z`)

| Requirement / Gate | Status | Direct Evidence Checked |
|---|---|---|
| **1. Predecessor `J2990` (`WW2 channel: merge the plan PR #989...`)** | **SATISFIED (`done` / merged)** | - Merged on `2026-11-17T19:37Z` via `orbit-with-ben` PR `#993` (`dbb4c802798a42f8827223fbab71afa227d88a90`), locking `WW2:001`–`WW2:003` topics on Ben's `17 Nov 17:20Z` go and committing `channels/ww2/studio/RULES.md` and `00_Brand/PLAYBOOK.md`. |
| **2. Predecessor `J2991` (`WW2 pilot 001: script and sources`)** | **DELIVERED (`done`), PRs `OPEN` awaiting Chief merge** | - `J2991` completed `2026-11-17T20:28Z`: 25-min script (`3,358` words, `20,431` spoken chars `<= 21,000` cap across 6 chapters), `SOURCES.md` (`8` primary UK/US official histories, `35/35` claim rows), separate `CLAIMS_CHECK_v01.md` (`35/35 PASS`), and `SHOT_LIST.md` (`46` shots / `50` timed windows).<br>- `orbit-with-ben` PR `#996` (`macbook/J2991` @ `24ca6adbfdd4fe959944b9fe2ba539fdd89bdde6`, `Rules check` `SUCCESS`) and mirrored `TheLaughingGod1986/ww2-channel` PR `#4` (`macbook/J2991` @ `4c5c0b0f3b82fbf6a467424f3c6f5c8e9bc0fe94`) are both still **`OPEN`** (`mergedAt: null`). |
| **3. Direct Predecessor `J2992` (`WW2 pilot 001: narration in Ben's voice`)** | **DELIVERED (`done`) & ON NAS, PRs `OPEN` awaiting Chief merge** | - `J2992` completed `2026-11-17T20:57Z`: verified on `/Volumes/data/studio-live/ww2/02_Video-Projects/001_Mulberry-Harbours-Floating-Ports-D-Day/02_Voiceover/` (`mulberry_harbours_vo_v01.wav` `318,086,478` bytes, `mulberry_harbours_vo_v01.mp3` `26,508,332` bytes, `mulberry_harbours_vo_v01_TAKE.json`, `vo_check.json`, `VO_REPORT.md`; `1,656.7 s` / `27:36.7`, `-19.7 LUFS`, `97.56%` normalized Scribe word match, `0` clipped boundary words).<br>- `orbit-with-ben` PR `#998` (`gemini/J2992-ww2-001-vo` @ `6ac5525f445f6cf98a07816be197f9b5ae51a7c3`, `Rules check` `SUCCESS`) and mirrored `TheLaughingGod1986/ww2-channel` PR `#2` (`gemini/J2992-ww2-001-vo` @ `847dfed7d28d4748d72e944539726819f281fb11`) are both still **`OPEN`** (`mergedAt: null`). |
| **4. `J2993` Checkpoint 6 (`orbit-with-ben` PR `#1012` @ `820c156807`) — Timing, Code Graphics & Thumbnails** | **PARTIAL (`1/5` steps done; timing & 16 draft graphics ready)** | - `gh pr view 1012`: `state: OPEN`, branch `codex/J2993-picture-prep`, head `820c15680718f417e07b9901bc1997b02951bb37` (`Rules check` `SUCCESS`), worktree `/Users/benjaminoats/_desk/ww2/J2993-wt`.<br>- **Audio anchors (`shot_anchors_v02.json`):** All `50` narration windows (`S01`–`S46b`, `0.160–1,656.700 s`) are exact-token aligned against Scribe timestamps (`resolve_anchors.py`).<br>- **Code graphics (`16` windows: `G1`–`G15` incl. `G11a`):** All 16 code-drawn maps and engineering diagrams exist as `1920x1080` `25 fps` `12 s` (`300`-frame) silent MP4 draft blocks on `/Volumes/data/studio-live/ww2/02_Video-Projects/001_Mulberry-Harbours-Floating-Ports-D-Day/03_Picture/` (`maps/`, `engineering_drafts_v01/`, `engineering_drafts_v02/`, `operational_maps_drafts_v01/`, `remaining_graphics_drafts_v01/`), with SHA-256 hashes verified (`graphic_coverage_v02.json`). Each 12 s block still needs expansion/intercut to span its full `23–45 s` narration paragraph without static holds/loops.<br>- **Thumbnails (`10_Thumbnail/`):** `ww2_001_thumb_A_archive_v01.jpg` and `ww2_001_thumb_B_floating_port_v01.jpg` are rendered on `studio-live` and passed `J3049` (`ww2-channel` PR `#11`) ad-safety screening. |
| **5. `J2993` Archive Photo Clearance (`34` archive windows in `PICTURE_COVERAGE_v06.md`) — Why `codex` Parked for Chief** | **BLOCKED ON CHIEF SCOPE RULING** | - Across 6 runs (`05:45Z`–`18:31Z`), `codex` downloaded `26` archive image files (`17` in `archive_editorial_review_v02.json` + `9` in `archive_retry_review_v03.json`, plus `80-G-286428_reference.jpg` in `storm_replacement_v01/`) to `/Users/benjaminoats/_desk/ww2/J2993/03_Picture/`.<br>- **Only 2 stills are currently marked `ELIGIBLE_FOR_EDIT_WITH_STATED_SUBJECT` in `ARCHIVE_PROVENANCE.md` / `archive_primary_review_v05.json`:** US Navy / NARA `80-G-285176` (`2951x2190`, LST-543 unloading at Mulberry A, window `S34`) and `80-G-285123` (`2941x2224`, Gooseberry blockship shelter off Omaha, window `S31`). A third US Navy photo, `80-G-286428` (storm damage with DUKWs beside roadway), is `REFERENCE_ONLY_LOW_RESOLUTION` (`740x620` HyperWar scan). Plus US Navy `80-G-285167` (`2944x2250`, LST-543 vehicle unloading) and `26-G-2963` (`2563x1929`, wave breaking over sunken-ship breakwater) are downloaded high-res NARA/USCG federal images.<br>- **Why the remaining windows are held (`J2993_CONTINUATION_v06.md`):**<br>  1. **`iwm.org.uk` HTTP 403 block:** Direct fetches to `www.iwm.org.uk/collections/item/object/...` return HTTP 403 from the Mac mini. The downloaded IWM files on Wikimedia Commons (`BU 1024` `4580x4590`, `B 5726` `1789x1772`, `A 24675` `2480x1673`, `A 25826` `1772x2302`, `H 40320` `1877x1772`, `A 24071` `2306x1748`, `A 25799` `2458x1748`, `H 35379` `2480x2485`, `H 32129` `2480x2480`, plus 800 px scans `A 24159`, `A 24678`, `A 24066`, `A 25814`, `A 24084`, `A 24115`, `H 32144`, `A 23738`) carry verbatim IWM Official Collection metadata (`War Office Second World War Official Collection` / `Admiralty Official Collection`, official military photographer, 1943–1944 creation -> UK Crown Copyright expired >50 years post-creation), but `codex` will not clear them without Chief authorisation to accept Commons' verbatim IWM Official Collection metadata + full-res visual check when `iwm.org.uk` returns 403.<br>  2. **Non-US/UK or mismatched items in `SHOT_LIST.md`:** `S04` (`LAC C-029878`, Canadian), `S10` (`TNA PREM 3/216/1`), `S23` (`Tate N05705` painting), `S43a`–`S44` (short `IWM T 29/30/31/32/54` PLUTO IDs), and `S35`–`S41b` (June 19–22 storm destruction, where original shot list misassigned unloading/Gooseberry photos) need Chief authorisation to use either sourced code-drawn technical/operational diagrams & maps (`AGENTS.md` *Missing footage fallback*) or alternative verified high-res US PD / UK Crown-expired archive photographs. |
| **6. Side-Effect Note: Cross-Channel `OWB:001` Board Leak (`J3068`)** | **IDENTIFIED (`PR #1021` pending)** | - Because `PR #1021` (`J3060`: `Prevent channel-qualified jobs from changing another channel film record`) is still `OPEN`, `codex` blocking `J2993` (`film: WW2:001`, `stage: edit`) in `a273ddc4b3` mutated `02_Video-Projects/001_Will-We-Ever-Meet-Aliens/status.json` (`OWB:001` `stages.edit.state = "blocked"`), which caused `6323c4401d` to spawn `J3068` (`Chief: resolve 001 edit orphan-blocked`). Merging `PR #1021` and resetting `OWB:001` `status.json` (as `J3013` did for `OWB:003` in `PR #1020`) resolves `J3014`, `J3015`, and `J3068`. |

---

## 3. Recommended Elected-Chief Action (`chief` / `codex`)

Because `J2993` was explicitly parked for the **Chief** (`J2993_CONTINUATION_v06.md`) and `scripts/jobs.py` enforces `Only the elected Chief may record a condition check` (`lines 533–534`) and `Only the elected Chief may release a verified hold` (`lines 963–964`), the elected Chief has two clean options:

### Option A (Recommended to keep WW2 Pilot 001 moving): Issue Chief Archive/Diagram Scope Ruling, Reopen `J2993` & Close `J3067`
Under `channels/ww2/studio/RULES.md` rule 5 and `AGENTS.md` *Missing footage fallback*, issue a Chief scope ruling authorising `codex` on `J2993` to:
1. **Clear the high-res IWM Official Collection photographs (`>=1748 px`) via verified Commons IWM Official Collection provenance + full-res visual inspection:** Where `iwm.org.uk` returns Cloudflare HTTP 403, verbatim IWM catalogue metadata on Wikimedia Commons confirming `War Office Second World War Official Collection` or `Admiralty Official Collection`, an official military photographer (`No. 5 AFPU` / Royal Navy official photographer), and a `1943`–`1944` creation date establishes expired UK Crown Copyright (>50 years under Copyright Act 1911 / CDPA 1988). Require full-resolution visual inspection and honest date/subject captions (`BU 1024` credited as Sept 1944 aerial view; `A 25799` Phoenix caisson tow; `H 35379` Phoenix construction; `B 5726` / `A 24675` / `A 25826` / `H 40320` / `A 24071` / `H 32129` matched strictly to their actual subjects).
2. **Use accurate sourced code-drawn engineering/operational diagrams & maps (`£0`, `draw_*.py`) or verified high-res US NARA / Navy / Signal Corps / USCG public-domain photographs (`80-G-285167`, `26-G-2963`, plus framed archival-plate insets for `740–800 px` references like `80-G-286428` / `SC 195881` / `A 23738` so no asset is upscaled above `2.35x`) for the remaining windows:** Specifically replace excluded `LAC C-029878` (`S04`), `Tate N05705` (`S23`), unresolved short PLUTO IDs (`S43a`–`S44`), and storm-damage windows (`S35`–`S41b`) with multi-beat code-drawn technical/operational graphics and properly framed archival plates, never presenting a code diagram as filmed evidence.
3. **Also merge (or authorise rebase with) `J2991` (`PR #996` / `ww2-channel#4`) and `J2992` (`PR #998` / `ww2-channel#2`).**

```bash
python3 scripts/jobs.py reopen J2993 --agent chief \
  --note "Chief ruling (J3067, jobs/reviews/J3067/REVIEW.md): (1) Predecessor J2992 narration mulberry_harbours_vo_v01 (1,656.7s) is verified on studio-live and all 50 Scribe anchors in shot_anchors_v02.json are locked. (2) Where iwm.org.uk returns HTTP 403, high-res (>=1748px) 1943-1944 War Office / Admiralty Official Collection photographs (BU 1024, B 5726, A 24675, A 25826, H 40320, A 24071, A 25799, H 35379, H 32129) and high-res NARA/US Navy/USCG photos (80-G-285176, 80-G-285167, 80-G-285123, 26-G-2963) are authorised for assembly once individually inspected at full resolution and labelled with their true date/subject (never dating Sept 1944 BU 1024 to 7 June). (3) For 740-800px archival scans (including 80-G-286428 storm reference, SC 195881, A 23738, A 24066, A 24084, A 24115, A 24159, A 24678, A 25814, H 32144), excluded non-US/UK items (LAC C-029878, Tate N05705), and unresolved PLUTO/storm windows, use framed archival-plate layouts (staying <=2.35x upscale) and expanded multi-beat sourced code-drawn technical/operational diagrams & maps (never presented as filmed evidence). Expand the 16 12s graphic blocks to match each sentence, assemble the full 1080p25 cut with a fresh WW2 score, run technical/QA checks, and stage for Ben's watch. £0." \
  --git

python3 scripts/jobs.py done J3067 --agent chief \
  --result "Verified J2993 condition (jobs/reviews/J3067/REVIEW.md): predecessor J2992 narration is complete on studio-live and 50 timing anchors + 16 draft code graphics are verified in PR #1012 (820c156807); issued Chief Missing-footage fallback & archive provenance scope ruling and reopened J2993 to complete picture coverage, full 1080p25 edit, WW2 score, QA and Ben-watch package. £0." \
  --git
```

### Option B: Keep `J2993` Blocked Pending Predecessor PR Merges (`#996`, `#998`) & Chief Ruling
If the Chief prefers to keep `J2993` held while reviewing `PR #996`, `PR #998`, and `PR #1012`:

```bash
python3 scripts/jobs.py wait J2993 --agent chief \
  --condition "Awaiting Chief Missing-footage fallback & archive provenance ruling for the 34 archive windows in PR #1012 (820c156807, J2993_CONTINUATION_v06.md; audited in J3067, jobs/reviews/J3067/REVIEW.md) and Chief merge of completed predecessor PRs #996/ww2-channel#4 (J2991 script/sources) and #998/ww2-channel#2 (J2992 VO)." \
  --check-at "2026-11-19T00:55:00Z" \
  --type input \
  --recheck J3067 \
  --action "Chief scopes archive fallback/code-diagram coverage for uncleared IWM/Navy windows and merges J2991/J2992 PRs, then codex finishes WW2:001 edit and score" \
  --git

python3 scripts/jobs.py done J3067 --agent chief \
  --result "Verified J2993 condition (jobs/reviews/J3067/REVIEW.md): NOT MET without Chief ruling — predecessor J2992 VO is on studio-live and 50 anchors + 16 code-graphic drafts are verified in PR #1012 (820c156807), but J2993 is parked for a Chief Missing-footage fallback / IWM-provenance ruling on the remaining archive windows and merge of predecessor PRs #996 (J2991) and #998 (J2992). J2993 kept blocked with --type input --recheck J3067 (next check 2026-11-19T00:55:00Z). £0." \
  --git
```
