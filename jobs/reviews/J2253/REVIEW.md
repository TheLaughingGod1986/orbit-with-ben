# J2253 Condition Verification Review — J1881 (`review Franklin eight-item correction recipe (+ film-wide captions) and scope production`)

- **Job**: `J2253` (`Verify condition for J1881`, `recheck_of: J1881`)
- **Parent Job**: `J1881` (`review Franklin eight-item correction recipe (+ film-wide captions) and scope production`)
- **Linked Predecessor Job**: `J2217` (`HOS 008 Franklin: amend J2163 correction recipe for four 5 Nov Ben notes + film-wide caption panels (GBP0)`, `status: done`, `done_ref: b78dbe19`)
- **Reviewer**: `gemini` (`gemini-argon` specialist worker; capabilities recorded in `chief_relay.py capabilities` as `''` — code/records/test verification only; no audio or moving-video perception claimed in this session)
- **Date**: `2026-11-05T21:08Z`
- **Verdict**: **CONDITION SATISFIED (`KEEP`) — All five J1881 elected-Chief FIX items are delivered and verified in `J2217` commit `b78dbe19b3f5ffee1cedad47bcc148d046dcf8bf` on HOS PR #428 (`cursor/J2217-eight-item`). Parked for elected Chief (`codex`) to release the verified hold on `J1881` (`jobs.py reopen J1881 --agent codex --note ... --git`) and complete the J1881 review/merge decision. `J2241` capability hold (`moving_video_input`) and `J2241` -> `J2242` -> `J2243` production dependencies remain preserved (`£0.00` / `0` credits).**

---

## 1. Waiting Condition on `J1881`

`J1881` was placed on a dependency hold at `2026-11-05T20:49Z` by the elected Chief (`codex`):
> `J2217 must deliver the five-point J1881 FIX on PR428: truthful GOP/capability evidence, P3 retake CLI/tests, explicit clock disposition, concrete caption treatment and real Flow preflight. Review immediately on delivery.`

---

## 2. Five-Point J1881 FIX Verification on HOS PR #428 (`b78dbe19`)

`J2217` completed at `2026-11-05T21:01Z` (`done_ref: b78dbe19`, commit `b78dbe19b3f5ffee1cedad47bcc148d046dcf8bf` on `origin/cursor/J2217-eight-item`). Each of the five required items in `jobs/reviews/J1881/REVIEW.md` (`Elected-Chief ruling — 5 November 2026 (Codex): FIX before production`) was independently verified on the Mac mini:

1. **Truthful GOP & Capability Evidence Level (`PASS`):**
   - `build_plan()` in `02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_build_rough_v13_recipe.py` renames `candidate_boundary_gop_envelope` to `candidate_keyframe_envelope` and explicitly records:
     - `gop_closure_proven: False`
     - `dependency_validation: "OUTSTANDING"`
     - `preservation: "Keep original PTS and durations. Unchanged decoded frames and audio stay identical. J2242 must prove both."`
     - `boundary_policy: "UNAPPROVED: candidate keyframe envelope only. Keyframe flags do not prove a closed GOP; dependency validation is outstanding. J2242 must prove dependencies and unchanged-frame/audio preservation before accepting output. Lossless only outside changed frames; no global re-encode."`
   - `J2163_CORRECTION_MANIFEST.json` (`schema: hos.uat_correction_plan.v4`), `J1868_UAT_CORRECTIONS.md`, and `J2217_AMEND.md` explicitly state that keyframe flags do not prove closed GOPs and that the planner uses the stored PTS list and cut list (`evidence_level: "source_map_only"`, `native_perception: false`) without claiming watched picture or heard audio.

2. **Missing `--retake-p3-01` & SHA-256 CLI / Validation Path & Tests (`PASS`):**
   - `_build_rough_v13_recipe.py` adds `--retake-p3-01` and `--retake-p3-01-sha256` to `main()`, sets `RETAKE_MIN_FRAMES = {'p2_02': 160, 'p5_13': 135, 'p3_01': 160}`, and validates `p3_01` in `verify_plan()`.
   - `test_retake_p3_01_missing_hash_and_short` in `test_j2163_recipe.py` verifies that a missing file, a mismatched SHA-256, or `< 160` decoded frames raises `PlanError` (CLI exit `2`), and `--execute` remains unconditionally refused (CLI exit `2`).

3. **Explicit `0:51` Disposition & Distinct `2:18` vs `2:20` Checks (`PASS`):**
   - **0:51 (`eight_rows[2]`):** Preserves Ben's exact verbatim note (`"still have hair flying out the tube, this needs rebuilt"`), sets `splice: false`, and adds `disposition`:
     - `ben_verbatim_kept: true`
     - `evidence_level: "source_map_only"`
     - `native_perception: false`
     - `night_street: "leave_untouched"`
     - `distinct_hot_night_rebuild: false`
     - `proposed_salon_retarget: "inference_pending_capable_in_context_confirmation"`
     - `note_resolved: false`
   - `splice_rows()` excludes `0:51` from `patches` (`len(patches) == 7`: `[[423, 544], [744, 839], [2506, 2665], [3168, 3343], [4511, 4670], [4977, 5077], [11358, 11492]]`).
   - **2:18 vs 2:20 (`eight_rows[4]`):** Keeps `jar_flip_2_18` (master frame `3305`, `138.000s`, inside replace `3260..3343` ending at `139.625s`, outside keep `3168..3259`) and `foil_next_spark_2_20` (master frame `3353`, `140.000s` = `1720320` ticks, `beyond_replacement_ending_139_625s: true`, `inside_replace_3260_3343: false`, `distinct_from_jar_flip: true`, `next_keyframe: 3344`, `candidate_keyframe_envelope: [3344, 3404]`, `gop_closure_proven: false`, `splice: false`, `note_resolved: false`) as two distinct unresolved checks.

4. **Concrete Planned Caption Treatment Table & Bottom-Text Reconciliation (`PASS`):**
   - `plan_captions()` converts the 27 `side_label` rows into **32 sequential planned cards** (splitting the 4 multi-phrase labels into `<= 4`-word sequential cards: `THE ANSWER IS` / `ON THE ROOF`, `A KITE` / `A KEY` / `A JAR`, `LET THE EXPERIMENT` / `BE MADE`, `PENNSYLVANIA GAZETTE` / `19 OCTOBER 1752`).
   - Every planned card enforces `word_count <= 4`, `hold_ticks <= 49152` (`<= 4s` static hold in `1/12288` master ticks, with any remainder recorded in `window_remainder_ticks`), non-overlapping master PTS intervals, `background: "unbordered umber"`, `border: False`, `gold_rule: False`, `pill_chrome: False`, `over: "moving plate"`, `one_at_a_time: True`, `rendered: False`, `new_claims: False`, and verifies all 4-digit years against `01_Script/FACT_NOTES_v01.md`.
   - `reconcile_bottom_text()` and `plan_safe_path()` explicitly set `side_label_inventory_proves_film_wide_coverage: False`, list the 8 code-graphic/overlay rows whose internal text is outside `side_label`, and separately plan `11_safe_path` (`SAFE PATH DOWN`, 3 words, `pts_in: 5665280`, `pts_end: 5706240`, `static_hold_s: "10/3"`, frame `11038`, `in_side_label_inventory: False`, `rendered: False`, `note_resolved: False`).

5. **Real Flow Spend Preflight (`PASS`):**
   - `spend_preflight()` verifies `/Users/benjaminoats/YouTube/orbit-with-ben/scripts/ai_spend.py` subcommands (`['record', 'spend', 'report', 'doc']`), explicitly rejects `ai_spend.py check` (`"not a subcommand; do not call it"`), and specifies:
     - Reading live Flow account balance via `read_account()` in `02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_mint_flow_cdp_v01.py` on CDP `ORBIT_FLOW_CDP` (`http://127.0.0.1:9222`, account `benoats@googlemail.com`) and logging with `ai_spend.py record --pool flow --left N`.
     - Reading the live Veo 3.1 Quality credit price on the Flow confirm dialog (`orbit_flow_veo_ui.py` matching `'Use N credits'`) prior to any Create.
     - Subtracting unposted `ai_spend.py` spends logged since the balance reading.
     - Enforcing `takes_max_per_plate: 3`, `subscription_credits_max_per_plate: 300`, `subscription_credits_max_total: 900`, `gbp: 0`, `no_top_up: True`, `no_overage: True`, `no_prepaid_ai_studio: True`, and `authorized: False`.

---

## 3. Independent Test, Dry-Run & CI Results (`b78dbe19`)

- **Unit Tests (`python3 -m unittest -v test_j2163_recipe.py`):** `Ran 18 tests in 0.277s — OK`
- **Read-Only Dry-Run (`python3 _build_rough_v13_recipe.py --dry-run`):** `status: "PLANNED_NOT_EXECUTABLE"`, master `cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b` and all `6/6` native source clips decode- and SHA-256-verified, `32` planned caption cards + `SAFE PATH DOWN` card, `spend_preflight` verified against `scripts/ai_spend.py`, `spend_gbp: 0`, `media_rendered: false`.
- **Repo Gate (`bash 00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/008_Lightning-Franklin`):** `ALL CHECKS PASS`
- **GitHub Actions CI on HOS PR #428 (`b78dbe19b3f5ffee1cedad47bcc148d046dcf8bf`):** `4/4` required checks `SUCCESS` (`Desk guard/no-desk-close`, `No media in git/no-media`, `Studio core check/check`, `Voice speed/atempo`).

---

## 4. Queue Disposition

- Under `scripts/jobs.py` (`do_reopen`), only the elected Chief (`codex`) may release a verified hold on `J1881`.
- `J2253` is therefore parked (`status: blocked`, `reason: "parked for Chief: ..."`) so the elected Chief (`codex`) can immediately release the hold on `J1881` (`python3 scripts/jobs.py reopen J1881 --agent codex --note "J2253 verified J2217 five-point FIX on HOS PR #428 b78dbe19 (jobs/reviews/J2253/REVIEW.md)" --git`), close `J2253`, and review `J1881`.
- All historical approvals (`h22`/`h35`, `J1297`, `master_v03` `cf1561c2...`), the `J1755` publication rejection, and the `J2241` `moving_video_input` capability hold remain untouched (`£0.00`).
