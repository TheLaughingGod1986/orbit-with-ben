# J2562 — the new Shorts check (straight-edge evidence) on thirteen real Shorts

- **Job:** J2562, follow-up to J2560 (orbit-with-ben #794; pair history-of-science #502). Run by `claudecode` on the Mac mini, 11 Nov 2026 about 08:55Z.
- **Scope:** read-only. Nothing re-cut, nothing changed in Studio, no change to the gate or its numbers. Spend: none.
- **Gate used:** `00_Brand/Channel-Setup/tools/gate_shorts_open.py`, sha256 `8ce0e9cb3726…`, byte-identical on `origin/main` of both repos (orbit-with-ben `d250dbf50e`, history-of-science `1fb86005`, which has #502). Each Short was run from a clean worktree of its own channel's repo at `origin/main`. The shared History of Science checkout on the Mini sits on another branch with the old gate, so it was not used.
- **Command, per Short:** `python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <file> --air-date <date> --id <id> --report-only --json`
- **Run record:** tmux `J2562-gate`, log `~/_desk/logs/J2562-gate.log`, exit file `~/_desk/logs/J2562-gate.done` (0), raw JSON `~/_desk/logs/J2562-results.json`. Every file's sha256 matches the one J2557 checked, so these are the same cuts.
- **The list:** the nine named in the brief plus the four the Chief added (Grok, 11 Nov 06:25Z, History of Science desk 6788769285): four Shorts the by-eye audit calls full frame, and all nine padded Orbit Shorts.

## Result

**Every Short came out as expected.** The four full-frame Shorts pass, each with one warning that names the seconds to look at. All nine padded Shorts still fail the rule. None of the nine stopped failing, so the park-for-Chief condition in the brief ("if any of the nine padded Shorts stops failing") is **not** triggered; the job is parked only as the brief's normal hand-over.

Three things for the Chief to weigh:

1. **Two padded Shorts now fail on the 15% figure alone.** `kKN8Ale42sE` (4 of 21, 19.0%) and `xdurJQcoiGM` (4 of 19, 21.1%) have no frame with a straight edge found: their blurred copies are feathered. They fail only because more than 15% of their frames look padded. The first is one frame over the line (3 of 21 would pass with a warning); the second is two over.
2. **The 15% figure has no room to spare on either side.** The highest full-frame Short, `Wvjd8g0CpzE`, has 3 padded-looking frames of 26 (11.5%) and 3 is the most it may have: one more soft frame and it fails again. The lowest padded Short, `kKN8Ale42sE`, is one frame above its limit. So on these thirteen the figure separates the two groups correctly, by one sampled frame each way.
3. **`bSjWiCbB7pY` passes only through the list of cuts Ben OK'd before the rule.** Its raw numbers: 12 of 27 frames padded (44.4%), all 12 with a straight edge, against the 10% limit. Without the list it fails.

## Table: one row per Short

Frames are sampled once a second; "sampled" is the frames outside any end card the cut's meta names. "Expected?" compares with step 4 of the brief.

| # | Id | Ch | Airs | By-eye audit | Sampled | Padded, with edge | Padded, no edge | Padded stretches (as the gate prints them) | Whole Short | Opening (0-0.5 s) | Rule that decides | Expected? |
|---:|---|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | `Wvjd8g0CpzE` | HOS | 2026-11-15 | full frame | 26 | 0 (0.0%) | 3 (11.5%) | 5-8 s (blur-pad, no edge) | **PASS** | PASS (0/3 padded, 0 with an edge) | none: under both limits | yes |
| 2 | `f17XCtUmN-g` | OWB | 2026-12-16 | full frame | 21 | 0 (0.0%) | 1 (4.8%) | 11-12 s (blur-pad, no edge) | **PASS** | PASS (0/3 padded, 0 with an edge) | none: under both limits | yes |
| 3 | `cLKDiYP55J8` | HOS | 2026-11-13 | full frame | 23 | 0 (0.0%) | 1 (4.3%) | 9-10 s (blur-pad, no edge) | **PASS** | PASS (0/3 padded, 0 with an edge) | none: under both limits | yes |
| 4 | `xgx2lYHhYZM` | HOS | 2026-11-17 | full frame | 25 | 0 (0.0%) | 1 (4.0%) | 14-15 s (blur-pad, no edge) | **PASS** | PASS (0/3 padded, 0 with an edge) | none: under both limits | yes |
| 5 | `kKN8Ale42sE` | OWB | 2026-11-17 | padded | 21 | 0 (0.0%) | 4 (19.0%) | 5-9 s (blur-pad, no edge) | **FAIL** | PASS (0/3 padded, 0 with an edge) | all-padded rule (over 15%) | yes |
| 6 | `xdurJQcoiGM` | OWB | 2026-11-25 | padded | 19 | 0 (0.0%) | 4 (21.1%) | 15-19 s (blur-pad, no edge) | **FAIL** | PASS (0/3 padded, 0 with an edge) | all-padded rule (over 15%) | yes |
| 7 | `rvug71d7Dqk` | OWB | 2026-11-21 | padded | 23 | 9 (39.1%) | 4 (17.4%) | 3-4 s (blur-pad), 11-23 s (blur-pad / blur-pad, no edge) | **FAIL** | PASS (0/3 padded, 0 with an edge) | edge rule (over 10%) and all-padded rule (over 15%) | yes |
| 8 | `C8lPx5N2DwM` | OWB | 2026-12-05 | padded | 33 | 12 (36.4%) | 8 (24.2%) | 9-12 s (blur-pad), 15-32 s (blur-pad / blur-pad, no edge) | **FAIL** | PASS (0/3 padded, 0 with an edge) | edge rule (over 10%) and all-padded rule (over 15%) | yes |
| 9 | `k2kEaA7ICjc` | OWB | 2026-12-11 | padded | 34 | 12 (35.3%) | 3 (8.8%) | 0-3 s (blur-pad / blur-pad, no edge), 13-19 s (blur-pad), 22-27 s (blur-pad), 33-34 s (blur-pad, no edge) | **FAIL** | FAIL (3/3 padded, 2 with an edge) | edge rule (over 10%) and all-padded rule (over 15%) | yes |
| 10 | `ffYKoNVPoqg` | OWB | 2026-11-10 | padded | 18 | 13 (72.2%) | 0 (0.0%) | 0-8 s (blur-pad), 13-18 s (blur-pad / mirror) | **FAIL** | FAIL (3/3 padded, 3 with an edge) | edge rule (over 10%) and all-padded rule (over 15%) | yes |
| 11 | `bSjWiCbB7pY` | OWB | 2026-11-13 | padded | 27 | 12 (44.4%) | 0 (0.0%) | 3-6 s (blur-pad), 10-19 s (blur-pad / mirror) | **PASS (raw rule FAIL; passes only by the OK'd-before-the-rule list)** | PASS (0/3 padded, 0 with an edge) | edge rule (over 10%) and all-padded rule (over 15%) | yes |
| 12 | `SWDCZfWZVao` | OWB | 2026-12-09 | padded | 23 | 6 (26.1%) | 4 (17.4%) | 3-6 s (blur-pad), 9-16 s (blur-pad / blur-pad, no edge) | **FAIL** | PASS (0/3 padded, 0 with an edge) | edge rule (over 10%) and all-padded rule (over 15%) | yes |
| 13 | `heiGCnGKTkE` | OWB | 2026-12-14 | padded | 24 | 9 (37.5%) | 0 (0.0%) | 6-9 s (blur-pad), 13-17 s (blur-pad), 20-22 s (blur-pad) | **FAIL** | PASS (0/3 padded, 0 with an edge) | edge rule (over 10%) and all-padded rule (over 15%) | yes |

End cards named in meta: only `f17XCtUmN-g` (20.92-22.36 s; 0 of its 2 end-card frames padded, left out of the 21). The other twelve name none, so every second counts as a shot.

## The gate's own verdict lines

### `Wvjd8g0CpzE` (HOS, airs 2026-11-15) — PASS

- File: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/10_Shorts/hos_005_s03_never_saw_v04.mp4` (sha256 `e1f862ba737a…`)
- warn: the picture may not fill 9:16 on 3/26 sampled frames: 5-8s (blur-pad, no edge). They are soft above and below a detailed middle, with no straight edge found, so this is not a FAIL: look at those seconds and say which it is
- Other warnings, not part of this check (1): [report-only] missing on-screen hook text at frame 0 (hook_edge 0.0000 < 0.005)
- No-edge frames, the two edge shares the gate measured (upper, lower; an edge needs 0.65): 5 s [0.407, 0.472], 6 s [0.361, 0.537], 7 s [0.352, 0.343]

### `f17XCtUmN-g` (OWB, airs 2026-12-16) — PASS

- File: `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/lift_oort_marbles/06_Final-Exports/028_short_lift_oort_marbles_v03.mp4` (sha256 `344bd0d0ab04…`)
- warn: the picture may not fill 9:16 on 1/21 sampled frames: 11-12s (blur-pad, no edge). They are soft above and below a detailed middle, with no straight edge found, so this is not a FAIL: look at those seconds and say which it is
- No-edge frames, the two edge shares the gate measured (upper, lower; an edge needs 0.65): 11 s [0.583, 0.63]

### `cLKDiYP55J8` (HOS, airs 2026-11-13) — PASS

- File: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/007_The-First-Vaccine/10_Shorts/hos_007_s04_smallpox_test_v04.mp4` (sha256 `3ef3fa773750…`)
- warn: the picture may not fill 9:16 on 1/23 sampled frames: 9-10s (blur-pad, no edge). They are soft above and below a detailed middle, with no straight edge found, so this is not a FAIL: look at those seconds and say which it is
- No-edge frames, the two edge shares the gate measured (upper, lower; an edge needs 0.65): 9 s [0.519, 0.417]

### `xgx2lYHhYZM` (HOS, airs 2026-11-17) — PASS

- File: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/007_The-First-Vaccine/10_Shorts/hos_007_s05_vacca_jesty_v05.mp4` (sha256 `e5ea76f012fb…`)
- warn: the picture may not fill 9:16 on 1/25 sampled frames: 14-15s (blur-pad, no edge). They are soft above and below a detailed middle, with no straight edge found, so this is not a FAIL: look at those seconds and say which it is
- No-edge frames, the two edge shares the gate measured (upper, lower; an edge needs 0.65): 14 s [0.509, 0.426]

### `kKN8Ale42sE` (OWB, airs 2026-11-17) — FAIL

- File: `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s8_voyager1_v01.mp4` (sha256 `b8bb56f7ef66…`)
- FAIL: the picture does not fill 9:16 on 4/21 frames sampled once a second (19.0%; 0 with a straight edge at the picture; limit 15% when no edge is found): 5-9s (blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- Other warnings, not part of this check (5): duration 20.7s outside 22–27s band; gap from last word to end is 3.00s > 1.5s (last word 17.74s, duration 20.74s); [report-only] pushed still at frame 0 (mean 0–1.5 s frame diff 0.33 < 1.50); [report-only] first cut at 4.60s > 3.0s (scene-change detect); [report-only] spoken text contains meta-promise ("stay, and i'll show you")
- No-edge frames, the two edge shares the gate measured (upper, lower; an edge needs 0.65): 5 s [0.5, 0.25], 6 s [0.509, 0.324], 7 s [0.324, 0.343], 8 s [0.315, 0.306]

### `xdurJQcoiGM` (OWB, airs 2026-11-25) — FAIL

- File: `00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/06_Final-Exports/owb_ar2_iss_2030_deorbit_v13.mp4` (sha256 `74aa35464bf2…`)
- FAIL: the picture does not fill 9:16 on 4/19 frames sampled once a second (21.1%; 0 with a straight edge at the picture; limit 15% when no edge is found): 15-19s (blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- Other warnings, not part of this check (1): duration 18.4s outside 22–27s band
- No-edge frames, the two edge shares the gate measured (upper, lower; an edge needs 0.65): 15 s [0.565, 0.481], 16 s [0.583, 0.426], 17 s [0.602, 0.417], 18 s [0.593, 0.417]

### `rvug71d7Dqk` (OWB, airs 2026-11-21) — FAIL

- File: `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/fri06_muons_ground_v04.mp4` (sha256 `06b935f706c8…`)
- FAIL: the picture does not fill 9:16 on 13/23 frames sampled once a second (57%, limit 10%): 3-4s (blur-pad), 11-23s (blur-pad / blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- No-edge frames, the two edge shares the gate measured (upper, lower; an edge needs 0.65): 19 s [0.315, 0.639], 20 s [0.37, 0.583], 21 s [0.343, 0.426], 22 s [0.361, 0.407]

### `C8lPx5N2DwM` (OWB, airs 2026-12-05) — FAIL

- File: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01.mp4` (sha256 `ebe11bb730cc…`)
- FAIL: the picture does not fill 9:16 on 20/33 frames sampled once a second (61%, limit 10%): 9-12s (blur-pad), 15-32s (blur-pad / blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- Other warnings, not part of this check (1): duration 33.0s outside 22–27s band
- No-edge frames, the two edge shares the gate measured (upper, lower; an edge needs 0.65): 15 s [0.435, 0.463], 16 s [0.417, 0.417], 18 s [0.519, 0.593], 20 s [0.519, 0.574], 22 s [0.389, 0.602], 23 s [0.519, 0.63], 24 s [0.639, 0.63], 27 s [0.481, 0.565]

### `k2kEaA7ICjc` (OWB, airs 2026-12-11) — FAIL

- File: `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/fri11_opening_testA/06_Final-Exports/029_short_fri11_opening_testA_v04.mp4` (sha256 `ff4194857a02…`)
- FAIL: frame 0 is not full-bleed 9:16: blur-pad above and below a picture band on 2/3 frames from 0.0 to 0.5 s (at 0.25s, sharp pixels above/middle/below 0%/8%/3%: no fine detail above or below, yet a picture's brightness is there) — reframe the opening shot to fill 1080x1920
- FAIL: the picture does not fill 9:16 on 15/34 frames sampled once a second (44%, limit 10%): 0-3s (blur-pad / blur-pad, no edge), 13-19s (blur-pad), 22-27s (blur-pad), 33-34s (blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- Other warnings, not part of this check (2): duration 33.9s outside 22–27s band; gap from last word to end is 2.32s > 1.5s (last word 31.58s, duration 33.90s)
- No-edge frames, the two edge shares the gate measured (upper, lower; an edge needs 0.65): 0 s [0.639, 0.398], 2 s [0.62, 0.38], 33 s [0.472, 0.454]

### `ffYKoNVPoqg` (OWB, airs 2026-11-10) — FAIL

- File: `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s6_titan_v11.mp4` (sha256 `8eead2f62fd3…`)
- FAIL: frame 0 is not full-bleed 9:16: blur-pad above and below a picture band on 3/3 frames from 0.0 to 0.5 s (at 0.00s, sharp pixels above/middle/below 0%/73%/2%: no fine detail above or below, yet a picture's brightness is there) — reframe the opening shot to fill 1080x1920
- FAIL: the picture does not fill 9:16 on 13/18 frames sampled once a second (72%, limit 10%): 0-8s (blur-pad), 13-18s (blur-pad / mirror) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- Other warnings, not part of this check (3): duration 18.0s outside 22–27s band; gap from last word to end is 1.87s > 1.5s (last word 16.13s, duration 18.00s); possible Orbit at 0 s (visor 0.0021)

### `bSjWiCbB7pY` (OWB, airs 2026-11-13) — PASS (raw rule FAIL; passes only by the OK'd-before-the-rule list)

- File: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/fri13_ingenuity_72_v06.mp4` (sha256 `54929328bd18…`)
- warn: the picture does not fill 9:16 on 12/27 frames sampled once a second (44%, limit 10%): 3-6s (blur-pad), 10-19s (blur-pad / mirror) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band) [not a FAIL for this file: OK'd before the rule (Ben, 10 Nov 2026 16:22Z, on the board; asked in J2510); a re-cut is not covered]
- Other warnings, not part of this check (1): gap from last word to end is 2.56s > 1.5s (last word 23.84s, duration 26.40s)

### `SWDCZfWZVao` (OWB, airs 2026-12-09) — FAIL

- File: `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/wed09_great_dimming/06_Final-Exports/029_short_wed09_great_dimming_v04.mp4` (sha256 `e0459b017dda…`)
- FAIL: the picture does not fill 9:16 on 10/23 frames sampled once a second (43%, limit 10%): 3-6s (blur-pad), 9-16s (blur-pad / blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- Other warnings, not part of this check (1): gap from last word to end is 2.29s > 1.5s (last word 20.41s, duration 22.70s)
- No-edge frames, the two edge shares the gate measured (upper, lower; an edge needs 0.65): 9 s [0.426, 0.407], 10 s [0.426, 0.389], 11 s [0.435, 0.417], 12 s [0.435, 0.407]

### `heiGCnGKTkE` (OWB, airs 2026-12-14) — FAIL

- File: `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/mon14_half_moon_daylight/06_Final-Exports/029_short_mon14_half_moon_daylight_v04.mp4` (sha256 `31f362f4437b…`)
- FAIL: the picture does not fill 9:16 on 9/24 frames sampled once a second (38%, limit 10%): 6-9s (blur-pad), 13-17s (blur-pad), 20-22s (blur-pad) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- Other warnings, not part of this check (1): gap from last word to end is 2.29s > 1.5s (last word 21.64s, duration 23.93s)

## How close each Short is to the two limits

"Frames to spare" is how many more padded frames a passing Short could take before failing, or how many fewer a failing Short would need to pass, on whichever rule is nearest.

| Id | By-eye | Edge frames / limit (10%) | All padded frames / limit (15%) | Frames to spare |
|---|---|---|---|---|
| `Wvjd8g0CpzE` | full frame | 0 / 2 allowed | 3 / 3 allowed | passes; 0 more padded frame(s) before a fail |
| `f17XCtUmN-g` | full frame | 0 / 2 allowed | 1 / 3 allowed | passes; 2 more padded frame(s) before a fail |
| `cLKDiYP55J8` | full frame | 0 / 2 allowed | 1 / 3 allowed | passes; 2 more padded frame(s) before a fail |
| `xgx2lYHhYZM` | full frame | 0 / 2 allowed | 1 / 3 allowed | passes; 2 more padded frame(s) before a fail |
| `kKN8Ale42sE` | padded | 0 / 2 allowed | 4 / 3 allowed | fails; would need 1 fewer padded frame(s) to pass |
| `xdurJQcoiGM` | padded | 0 / 1 allowed | 4 / 2 allowed | fails; would need 2 fewer padded frame(s) to pass |
| `rvug71d7Dqk` | padded | 9 / 2 allowed | 13 / 3 allowed | fails; would need 10 fewer padded frame(s) to pass |
| `C8lPx5N2DwM` | padded | 12 / 3 allowed | 20 / 4 allowed | fails; would need 16 fewer padded frame(s) to pass |
| `k2kEaA7ICjc` | padded | 12 / 3 allowed | 15 / 5 allowed | fails; would need 10 fewer padded frame(s) to pass |
| `ffYKoNVPoqg` | padded | 13 / 1 allowed | 13 / 2 allowed | fails; would need 12 fewer padded frame(s) to pass |
| `bSjWiCbB7pY` | padded | 12 / 2 allowed | 12 / 4 allowed | fails; would need 10 fewer padded frame(s) to pass |
| `SWDCZfWZVao` | padded | 6 / 2 allowed | 10 / 3 allowed | fails; would need 7 fewer padded frame(s) to pass |
| `heiGCnGKTkE` | padded | 9 / 2 allowed | 9 / 3 allowed | fails; would need 7 fewer padded frame(s) to pass |

## What was not done

- No grey 108 x 192 frames are saved: the brief asks for them only for a Short that did not come out as expected, and none did.
- Nobody watched the Shorts in this job. The by-eye column is J2545's audit; this job only ran the check and counted.
- The warned seconds on the four full-frame Shorts (`Wvjd8g0CpzE` 5-8 s, `f17XCtUmN-g` 11-12 s, `cLKDiYP55J8` 9-10 s, `xgx2lYHhYZM` 14-15 s) are the same frames J2557 described as full-frame shots with soft tops and bottoms.
