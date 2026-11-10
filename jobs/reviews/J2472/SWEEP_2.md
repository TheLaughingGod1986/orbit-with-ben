# J2472 — PR Backlog Sweep, Part 2 (`SWEEP_2.md`)

**Agent:** `macbook-2` · **Date:** `2026-11-10`

## Summary (one line per item)

1. **`#604` (`gemini/J2325`) → READY (`b9842cabc`); `#611` (`cursor/J2335-pluto-pickup`) → STOPPED (waiting for Chief to merge `#604` first):** Merged `origin/main` into `gemini/J2325` (`#604`), keeping `main`'s two `J1100` rows in `04_Audio/elevenlabs_ledger.jsonl` and appending `#604`'s `pluto_frozen_heart_vo_v01` row (`8001` chars; `05_Analytics/ai_spend/ledger.jsonl` already has its 3 `J2157` rows on `main`), all checks PASS; stopped before `#611` per brief so Chief can merge `#604` first and the next pass can merge the updated `main` into `#611` and re-append only its own 2 pickup rows.
2. **`#676` (`macbook/J2374`, weekly Orbit thumbnail audit) → READY (`88e2cab81`):** Merged `origin/main` into `macbook/J2374`, kept `main`'s `T023` (HOS 002) and renumbered `J2374`'s three OWB draft Bs to `T024`, `T025`, `T026` in `05_Analytics/tests/THUMB_LEDGER.json`, kept both `9 Nov HOS update (J2397)` and `9 Nov OWB update (J2374)` in `05_Analytics/weekly_thumb_audit/PATTERNS.md`, and verified `thumb_ledger.py verdict` + all repo checks PASS.
3. **`#311` (`codex/J1090`, 025 opening Short v07; contains `#310`'s files) → READY (`9aa2b8cdf`, Chief can close `#310`):** Merged `origin/main` into `codex/J1090`, confirmed `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/wed11_opening_testA/06_Final-Exports/sha256_manifest.json` still names `"stem": "wed11_opening_testA_v05"` as the uploaded file, and verified all repo checks + `py_compile` PASS.
4. **`#653` (`macbook/J2411`, HOS 100 & 101 into waiting line) → READY via replacement PR `#696` (`macbook/J2472-wip-hos-100-101`, `dd752c703`) + queued job `J2473` (Chief can close `#653`):** Queued the Rule-E review job for HOS PR `#460` (`HOS:100` Bird Magnetic Compass & `HOS:101` Deep-Sea Hydrothermal Vents) via `jobs.py add --git` on `main` (assigned new ID **`J2473`**), and opened fresh PR **`#696`** adding `"HOS:100"` and `"HOS:101"` to `next_hos` in `jobs/WIP.json` (`test_channels.py`, `test_workflow_handoffs.py`, and all repo checks PASS).
5. **`#645` (`macbook/J2373`, 8 HOS Shorts lab rows and 3 learnings) → READY (`edbfc3dde`):** Merged `origin/main` into `macbook/J2373`, kept all 8 HOS Shorts lab rows and all 3 HOS learnings (none only repeat rows 24–26: HOS `J0955` loop-tail/hold re-cut validation + Frame-0 hero-object specificity, HOS Shorts curriculum search-intent titles, and HOS 4 Shorts/week + Saturday 11:30 go-public-day Short), renumbered them to rows **27, 28, 29** after `main`'s row 26, and verified all repo checks PASS.
6. **`#554` (`macbook/J2204`, `HOS-2026-11-E2`, proof-first first 30 seconds) → READY (`acdf4a9bd`; merge `#645` first or refresh alongside `#611`):** Merged `origin/main` into `macbook/J2204`, kept `05_Analytics/tests/HOS_LONG_TESTS.md`, renumbered its `05_Analytics/LEARNINGS.md` row to **30** (following `#645`'s rows 27–29), and verified all repo checks PASS. *(Note: because `#645` and `#554` both append right after row 26 in `05_Analytics/LEARNINGS.md` against `origin/main`, once Chief merges `#645` along with `#604`, `#554` can be refreshed with `origin/main` right alongside `#611` if GitHub marks the adjacent line conflicting.)*
7. **`#552` (`macbook/J2203`, `HOS-2026-11-E1`, anomaly-first Short gate) → STOPPED (contradicts Rule 24, "The first second", `J2429`; left for Chief):** Not re-applied because `--hos-anomaly-first` (`b1e11f8c5`) contradicts Rule 24 (`LEARNINGS.md` row 24 / `.cursor/rules/orbit-build-shorts.mdc`) in four ways:
   - **Spoken hook window (`2.0 s` / `2.85 s` vs `≤ 1.5 s`):** `#552` sets `E1_WORD4_BY = 2.0` (allowing words 1–4 up to `2.0 s` and 010 Short A sentence 1 to `2.85 s`), whereas Rule 24 requires the subject noun + surprise word completed `≤ 1.5 s` (`vo_onset_s ≤ 0.15 s`).
   - **Pronoun opener (`"This..."`) vs named subject noun:** `#552`'s `e1_open_verdict` only bans `"In <year>,"` and bare biographer names, and its canonical passing test `OPEN` in `test_gate_e1.py` starts with `"This thin line of clay marks the end"` (`("This", 0.05, 0.25)`), whereas Rule 24 bans unanchored pronoun openers (`zero pronoun opener "This planet/star..."`).
   - **VO pause ceiling (`0.25 s` vs `0.15 s`):** `#552` sets `E1_PAUSE_MAX = 0.25` across `0–5 s` (`test_gate_e1.py` passes a `0.20 s` pause at `1.0–1.2 s`), whereas Rule 24 / the 60% rule allows no pause `> 0.15 s` in sentence 1 (`0–1.5 s`).
   - **Cut 1 minimum floor (`1.8–2.5 s` vs `≤ 2.8–3.0 s`):** `#552`'s `e1_cut_verdict` hard-FAILs any Cut 1 earlier than `1.8 s` (`E1_CUT1_LO = 1.8`, failing `cut1 = 1.2 s`), whereas Rule 24 / first-two-seconds rules require a visible change by `~1.0 s` and Cut 1 `≤ 2.8–3.0 s` with no `1.8 s` minimum floor.

## Left alone per brief

- `#368`, `#490` (Chief reviews code changes), `#333` (draft), `#666`.

## Check outputs on touched branches

- `python3 scripts/sync_rules.py --check` → `rules OK`
- `python3 scripts/studio.py status --check` → `STATUS.md OK`
- `python3 scripts/core_sync.py check` → `core OK (56 shared files)`
