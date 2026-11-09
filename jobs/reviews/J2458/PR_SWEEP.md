# J2458 — PR Backlog Sweep (48 Open PRs vs `main` at `6b8307a73`)

Sweep date: `2026-11-09` (`macbook` worker).
Repo-wide checks run across updated `MERGE` branches:
- `python3 scripts/sync_rules.py --check` -> `rules OK`
- `python3 scripts/studio.py status --check` -> `STATUS.md OK`
- `python3 scripts/core_sync.py check` -> `core OK (56 shared files)`

Summary of the 48 PRs (`#666` and `#676` skipped per brief; no PR merged or closed by worker):
- **`CLOSE` (18 PRs):** `#310, #311, #323, #338, #501, #502, #517, #539, #551, #555, #562, #564, #569, #571, #572, #575, #600, #650`
- **`MERGE` (23 PRs, updated with `origin/main` and pushed):** `#283, #295, #301, #303, #314, #324, #354, #357, #359, #368, #381, #385, #388, #490, #493, #532, #553, #557, #604, #609, #611, #642, #653`
- **`CHIEF` (7 PRs, needs Chief decision on overlapping rules/code):** `#261, #291, #487, #519, #552, #554, #645`

---

## 1. `CLOSE` — Already on `main` (18 PRs)

- **#310** (`codex/J1084` — *025: rebuild opening Short final Mars shot (v06)*): Already on `main` (`cuts_v06.json`, `picture_qa_v06`, `polish_gate_v06`, `sha256_manifest_v06.json`, `wed11_opening_testA_v06_*` and `v07` landed in `1295111c0` / `1ecbea05c`; `sha256_manifest.json` stays on uploaded `v05` per `e72be473a`).
- **#311** (`codex/J1090` — *025: rebuild opening Short final Mars shot (v07)*): Already on `main` (`06_Final-Exports/*_v07*`, `sha256_manifest_v07.json`, `jobs/reviews/J1090/J1093_DIRECT_AUDIO_AND_UAT_VERIFICATION_2026-10-28.md` and `jobs/reviews/J1090/evidence/*` landed in `1295111c0` and `1ecbea05c`; `sha256_manifest.json` stays on uploaded `v05` per `e72be473a`).
- **#323** (`codex/j1107-thumb-audit` — *J1107: checkpoint baseline before live HOS Studio read*): Superseded by `#324` (`codex/j1107-hos-thumb-audit`, full 3-commit 28 Oct HOS report on the same path `05_Analytics/weekly_thumb_audit/HOS/2026-10-28.md`) and `main` commit `d75b56ed6` (`J2397` 9 Nov HOS audit).
- **#338** (`codex/j1129-ledger` — *HOS 002: record applied thumbnail in THUMB_LEDGER (J1129)*): Already on `main` as `T023` in `05_Analytics/tests/THUMB_LEDGER.json` (`d75b56ed6`, `video: "AL_-qlWko_g"`, `job: "J1129"`, with full sha256 and 9 Nov Studio read-back).
- **#501** (`codex/j2143-thumbnails` — *031: build three thumbnail concepts (J2143)*): Already on `main` via `765d77f8f` (`J2166: KEEP review of 031 thumbnails (J2143) and land T021 ledger/evidence`; `PROMPTS.json`, `inputs.json`, `measurements.json`, `build_j2143.py` are byte-identical on `main`, and `REVIEW.md` / `THUMB_LEDGER.json` carry the later `J2166` KEEP review).
- **#502** (`codex/J2155-uranus-vo` — *033: generate full narration VO take (J2155)*): All 5 `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/02_Voiceover/` files (`J2155_VO_CHECKS_v01.json`, `J2155_VO_REVIEW_v01.md`, `uranus_vo_v01_TAKE.json`, `stt/uranus_vo_v01/stt_raw.json`, `words.srt`) and the `04_Audio/elevenlabs_ledger.jsonl` row (`uranus_vo_v01`, `7858` chars) are byte-identical on `main`.
- **#517** (`codex/J2089-run-1105` — *032: complete remaining process graphics exports (J2089)*): Superseded on `main` by PR `#538` (`22532c173`, `032: complete reviewed process overlay exports (J2089)`) and `7920d0f77` (`J2378/J2089` Chief PASS with `PROCESS_*_v03.json` and `J2089_CHECKPOINT_v07.md`..`v33.md`).
- **#539** (`worker/J2141-opening-v01` — *031: render opening code graphics and space-weather harvest (J2141)*): Consolidated into PR `#633` and merged to `main` in `ae085e857` (`031: merge J2141 £0 picture package & acting-Chief gate resolution`) and `f93b617a3` (`J2387` v02 master).
- **#551** (`worker/J2141-field-v01` — *031: render field and magnetosphere code graphics (J2141)*): Merged to `main` in `ae085e857` (PR `#633`); `CODE_FIELD_v01.json`, `CODE_FIELD_TECHNICAL_CHECK_v01.json`, and `field_graphics.py` are byte-identical on `main`.
- **#555** (`worker/J2141-saa-v01` — *031: render South Atlantic Anomaly and Swarm code graphics (J2141)*): Consolidated and superseded on `main` in `ae085e857` (PR `#633`, `CODE_SAA_v01.json`, `saa_graphics.py`).
- **#562** (`worker/J2141-dynamo-v01` — *031: render outer-core dynamo and reversal-model code graphics (J2141)*): Consolidated and superseded on `main` in `ae085e857` (PR `#633`, `CODE_DYNAMO_v01.json`, `dynamo_graphics.py`).
- **#564** (`worker/J2141-sky-v01` — *031: render sky, aurora, and ozone code graphics (J2141)*): Consolidated on `main` in `ae085e857` (PR `#633`; `CODE_SKY_v01.json` and `CODE_SKY_TECHNICAL_CHECK_v01.json` byte-identical on `main`, `sky_graphics.py` updated in `ae085e857`).
- **#569** (`worker/J2141-core-v01` — *031: render inner-core rescue and survival code graphics (J2141)*): Consolidated on `main` in `ae085e857` (PR `#633`; `CODE_CORE_v01.json` and `CODE_CORE_TECHNICAL_CHECK_v01.json` byte-identical on `main`, `core_graphics.py` updated in `ae085e857`).
- **#571** (`worker/J2141-timeline-v01` — *031: render timeline, paleomagnetic, and WHO/FACT overlays (J2141)*): Consolidated on `main` in `ae085e857` (PR `#633`; `timeline_graphics.py` and `CODE_TIMELINE_TECHNICAL_CHECK_v01.json` byte-identical on `main`, paired with `CODE_TIMELINE_MACBOOK_v01.json`).
- **#572** (`worker/J2141-commons-v01` — *031: harvest Wikimedia kauri, hand-stencil, and nature plates (J2141)*): Consolidated on `main` in `ae085e857` and `f93b617a3` (`harvest_commons_nature.py` and `HARVEST_COMMONS_TECHNICAL_CHECK_v01.json` byte-identical on `main`, `HARVEST_POOL_v01.json` updated in `f93b617a3`).
- **#575** (`worker/J2141-integrated-v01` — *031: integrate J2141 code-graphics and harvest batches (opening..commons)*): Consolidated and superseded on `main` by `ae085e857` (PR `#633`, 169 files) and `f93b617a3` (`J2387` v02 master).
- **#600** (`macbook/J2223` — *J2223: Lock 3 Short titles and angles for OWB 033 (Uranus) and 034 (Pluto)*): Already on `main` (`033/10_Shorts/SHORTS_PLAN_v01.md` byte-identical via `576cc7951` `J2317`; `034/10_Shorts/README.md` and `SHORTS_PLAN_v01.md` updated via `eba41b11c` `J2360` `#632`; `production-status.md` and `film_briefs.json` at later versions `2f27b57df`, `3c0ebf132`, `b75ef47fe`).
- **#650** (`macbook/J2410` — *J2410: add OWB 062 (Phobos crash) and 063 (Saturn Hexagon) topic briefs from data*): Already on `main` via `dfde63f2a` (`J2410: add OWB 062 (Phobos crash) and 063 (Saturn Hexagon) topic briefs from data`) and advanced by `a32bdf467` (`J2420` Rule-E topic go/no-go review).

---

## 2. `MERGE` — Brought Up to Date with `origin/main` and Pushed (23 PRs)

- **#283** (`codex/j0963-sun-brighter` -> `8665f5bc2`): Merged `origin/main` cleanly; diff is `00_Brand/Channel-Setup/tests/long_thumbs_2026_10/j0963_sun_tc_b_v02.json` and `scripts/build_sun_venus_tc_b_j0908.py` (`py_compile` + `sync_rules`/`studio status`/`core_sync` PASS).
- **#295** (`codex/j0915-review-20261026` -> `316dfbbbd`): Merged `origin/main` cleanly; diff is `jobs/reviews/J0915_2026-10-26.md` (repo checks PASS).
- **#301** (`codex-j1027` -> `317eb6be6`): Merged `origin/main` cleanly; diff is `jobs/readbacks/J1027.json` (repo checks PASS).
- **#303** (`codex-j1031` -> `3faeb9c52`): Merged `origin/main` cleanly; diff is `jobs/readbacks/J1031.json` (repo checks PASS).
- **#314** (`codex/J1102` -> `01c178657`): Merged `origin/main`, kept `main`'s `queue.json`, `UPLOADS.json`, and `library.json` (which already record `xvarZP2aYyE`), and preserved all 12 `J1102_v04_swap/*`, `jobs/readbacks/J1102*`, and `jobs/reviews/J1102_delivery_2026-10-28.md` evidence files (repo checks PASS).
- **#324** (`codex/j1107-hos-thumb-audit` -> `0e10665c5`): Merged `origin/main`, kept `main`'s `THUMB_LEDGER.json` and `PATTERNS.md` (`d75b56ed6`), and preserved `05_Analytics/weekly_thumb_audit/HOS/2026-10-28.md` (repo checks PASS).
- **#354** (`gemini/j0978-test-b-readback` -> `64b43f7b0`): Merged `origin/main` cleanly; diff is `05_Analytics/tests/STUDIO_TESTS.md` and `05_Analytics/tests/test_b_apply_readback.json` (repo checks PASS).
- **#357** (`codex/j1269-verify` -> `fd62971b6`): Merged `origin/main` cleanly; diff is `jobs/readbacks/J1269.json` (repo checks PASS).
- **#359** (`codex/J1100-resume-1031` -> `8bfead9a1`): Merged `origin/main`, kept `main`'s `05_Analytics/ai_spend/ledger.jsonl` (already contains `J1100_s2_open_pickup_v01` and `J1100_s5_open_pickup_v01`), appended the 2 `J1100` rows to `04_Audio/elevenlabs_ledger.jsonl`, and kept all 8 `jobs/reviews/J1100/resume_1031/*` files (repo checks PASS).
- **#368** (`codex/J1333-watch` -> `d9070511f`): Merged `origin/main` into `scripts/kanban_snapshot.py`, `scripts/test_watch_links.py`, `05_Analytics/kanban/watch_uploads.json`, and `jobs/reviews/J1333/*`; `python3 -m unittest scripts/test_watch_links.py` PASS (`Ran 12 tests in 0.055s — OK`) + repo checks PASS.
- **#381** (`codex/j1630-atom-verification` -> `6a0602ea9`): Merged `origin/main`; diff is `jobs/readbacks/J1630.json` (repo checks PASS).
- **#385** (`codex/j1663-title-test-check` -> `f6dc6fdb5`): Merged `origin/main`; diff is `jobs/readbacks/J1663.json` (repo checks PASS).
- **#388** (`codex/j1700-readback` -> `c61a7ea69`): Merged `origin/main`; diff is `jobs/readbacks/J1700.json` (repo checks PASS).
- **#490** (`codex/j2040-allowlist` -> `f521bcd3f`): Merged `origin/main` with all 21 `J2040` allowlist scripts, docs, evidence, and tests; `python3 -m unittest scripts/test_codex_scoped_push.py` (`Ran 3 tests — OK`) and `python3 -m unittest discover -s 07_Content-Ops/tests -p 'test_codex_*.py'` (`Ran 51 tests — OK`) + repo checks PASS.
- **#493** (`codex/J2022-finish` -> `7ed87d759`): Merged `origin/main` (keeping `main`'s updated `scripts/ai_spend_daily.py` which already has `reuse_page` and `04f33f2f7`'s retirement of `apply_packaging_long_thumbs_j0133.py`, plus `#493`'s `jobs/reviews/J2022/WORKER_NOTE.md`, `scripts/apply_melodysheep_long_thumbs_v01.py`, and `scripts/apply_yellow_white_v04_thumbs.py`); `python3 -m unittest scripts/test_ai_spend_daily.py scripts/test_cdp_tabs.py` PASS (`Ran 21 tests in 0.007s — OK`) + repo checks PASS.
- **#532** (`macbook/J2215` -> `f7e0fb0df`): Merged `origin/main` cleanly; diff is `jobs/reviews/J2215/REVIEW.md` (repo checks PASS).
- **#553** (`macbook/J2219` -> `f0f1254dc`): Merged `origin/main` cleanly; diff is `02_Video-Projects/J01_Journey-To-Every-World/11_Upload-Package/Descriptions/j01_description_v01.txt` and `jobs/reviews/J2219/REVIEW.md` (repo checks PASS).
- **#557** (`cursor/J2202-studio-reach` -> `18710f881`): Merged `origin/main` cleanly; `python3 -m unittest scripts/test_studio_reach.py` PASS (`Ran 9 tests in 0.003s — OK`) + repo checks PASS.
- **#604** (`gemini/J2325` -> `113cc8941`): Merged `origin/main`, appended `pluto_frozen_heart_vo_v01` rows to `04_Audio/elevenlabs_ledger.jsonl` and `05_Analytics/ai_spend/ledger.jsonl`, and preserved all 12 `034` VO/STT and `jobs/reviews/J2157` + `J2325` files (repo checks PASS).
- **#609** (`macbook/J2327` -> `7268d0fea`): Merged `origin/main` cleanly; diff is OWB 035–038 `TOPIC_GO_NO_GO.md` sheets, `production-status.md`, and `jobs/reviews/J2327/REVIEW.md` (repo checks PASS).
- **#611** (`cursor/J2335-pluto-pickup` -> `12d8377fa`): Merged `origin/main`, appended `pluto_ch05_looked_back_v02` rows to `04_Audio/elevenlabs_ledger.jsonl` and `05_Analytics/ai_spend/ledger.jsonl`, and preserved all 6 `034` pickup files and `jobs/reviews/J2335/EVIDENCE.md` (repo checks PASS).
- **#642** (`macbook/J2369` -> `846f4a264`): Merged `origin/main` cleanly; diff is `02_Video-Projects/_dated_shorts/2026-11-24_supermoon-two-earths-closer.md` (repo checks PASS).
- **#653** (`macbook/J2411` -> `c21ce1f2a`): Merged `origin/main`, kept `main`'s `WIP.json` and `queue.json`, appended `HOS:100` and `HOS:101` to `jobs/WIP.json` `next_hos`, and re-queued the J2411 Rule-E review job via `scripts/jobs.py add` as `J2463` (repo checks PASS).

---

## 3. `CHIEF` — Needs a Decision (7 PRs)

- **#261** (`codex/j0874-shorts-learnings` — *rules(shorts): encode J0871 approved learnings checklist (J0874)*): Modifies `.cursor/rules/orbit-build-shorts.mdc` and `02_Video-Projects/_template_NNN_Episode-Slug/10_Shorts/README.md`, which were later expanded on `main` by `J0900`/`J0907`, `OWB-2026-11-E1` (6 Nov), and `J2429` (9 Nov, `4cb58491f`).
  **Choice:** Close `#261` because `main` already includes `## Approved Learnings checklist — Chief, J0871 / J0874 / J0900 / J0907` plus the November Shorts rules (`sync_rules.py --check` PASS on `main`), or cherry-pick only the `_template_NNN_Episode-Slug/10_Shorts/README.md` checklist table if still wanted.
- **#291** (`grok/audit26-rules` — *Encode 26 Oct Orbit audit rules + add plate_check.py*): Modifies `AGENTS.md`, `STUDIO_PLAYBOOK.md`, `.cursor/rules/orbit-build-shorts.mdc`, `orbit-build-long.mdc`, `orbit-studio.mdc`, `scripts/sync_rules.py`, and `.github/workflows/rules-check.yml`, encoding the 26 Oct "end card with title + yellow long id" Shorts rule that was overtaken by November's zero-end-card `<1.0 s` loop-tail rule (`OWB-2026-11-E1`) and `J2428`/`J2429`.
  **Choice:** Close `#291` as overtaken by the November long/Shorts rules, or cherry-pick only `00_Brand/Channel-Setup/tools/plate_check.py`, `test_plate_check.py`, and `AUDIT_2026-10-26_CANDIDATES.md` without the superseded rule edits.
- **#487** (`codex/j2022-tab-reuse` — *cdp: reuse existing tab in remaining Studio/spend scripts (J2022)*): Modifies the exact same 4 scripts as `#493` (`codex/J2022-finish`), which is the completed 2-commit version of `J2022` (including `jobs/reviews/J2022/WORKER_NOTE.md`) now updated and tested under `MERGE`.
  **Choice:** Close `#487` as superseded by `#493` (`codex/J2022-finish`), and merge `#493`.
- **#519** (`claude/fervent-meitner-2snnro` — *jobs: release a held job the agent can't resume, then pick normally*): Modifies `choose_next` and `do_next` in `scripts/jobs.py` to release a held job with an external hold / capability problem (`5 Nov 2026: Gemini sat on J1100`), which `main` also implemented directly in `choose_next` using `if workflow.role_job(held): return None`.
  **Choice:** Close `#519` and keep `main`'s simpler in-place `choose_next` release logic, or adopt `#519`'s `released: list | None` parameter + `chief_relay.current_execution(at)` lease guard.
- **#552** (`macbook/J2203` — *HOS-2026-11-E1: anomaly-first Short gate for films 008–010 (J2203)*): Modifies shared core file `00_Brand/Channel-Setup/tools/gate_shorts_open.py`, `studio-core/CORE_FILES.json`, `.github/workflows/rules-check.yml`, and `05_Analytics/LEARNINGS.md` (row 23), conflicting with `4cb58491f` (`J2429` Orbit Shorts first-second gate on `gate_shorts_open.py` and `CORE_FILES.json`) and `66ad39d51` (`J2428–J2430` rows 23–26 in `LEARNINGS.md`).
  **Choice:** Re-apply `#552`'s `--hos-anomaly-first` flag onto `4cb58491f`'s `gate_shorts_open.py` (with a fresh `core_sync.py` hash and `LEARNINGS.md` row 27), or close `#552` if `J2429`/`J2430` supersede `HOS-2026-11-E1`.
- **#554** (`macbook/J2204` — *HOS-2026-11-E2: proof-first first 30 seconds on longs 008–010 (J2204)*): Adds `HOS-2026-11-E2` as row 24 in `05_Analytics/LEARNINGS.md` plus `05_Analytics/tests/HOS_LONG_TESTS.md` and `jobs/reviews/J2204/REVIEW.md`, colliding with `main`'s rows 23–26 (`J2428` OWB first-30s hook and `J2430` row 25 *Title question in the first 5 seconds of HOS longs*).
  **Choice:** Merge `#554` with its `LEARNINGS.md` entry renumbered after row 26 alongside `HOS_LONG_TESTS.md`, or close `#554` if `J2430` row 25 supersedes the `HOS-2026-11-E2` 008–010 test entry.
- **#645** (`macbook/J2373` — *J2373: Add 8 HOS Shorts lab rows (26 Oct – 5 Nov) and 3 HOS learnings rules/tests*): Adds 8 HOS Shorts lab rows and 3 new rule/test rows (numbered 23–25) in `05_Analytics/LEARNINGS.md` plus `jobs/reviews/J2373/REVIEW.md`, colliding with `main`'s rows 23–26 from `J2428–J2430`.
  **Choice:** Merge `#645` keeping the 8 HOS Shorts lab table rows and renumbering its 3 `LEARNINGS.md` rows to 27–29 (or deduplicating against rows 24–26), or close `#645` if `J2429`/`J2430` replace those rules.
