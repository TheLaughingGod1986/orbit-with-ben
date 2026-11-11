# J2594 — the thirteen real Shorts rerun with the twice-a-second count (orbit-with-ben #817)

- **Job:** J2594, step 3 of J2579 (Grok's ruling, History of Science desk 6791598029). Run by `claudecode` on the Mac mini, 11 Nov 2026 about 11:15Z.
- **Scope:** read-only. Nothing re-cut, nothing changed in Studio, no change to the gate or its figures. Spend: none.
- **Gate used, for all thirteen (History of Science's too):** the Orbit With Ben copy on branch `claude/youtube-channel-audit-pa4n3b` at commit `67cb29f531`, in a clean worktree. `00_Brand/Channel-Setup/tools/gate_shorts_open.py` sha256 `f37031aeec42…`. `python3 scripts/core_sync.py check` passes there (core OK, 56 shared files).
- **Command, per Short:** `python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <file> --air-date <date> --id <id> --report-only --json`
- **Same cuts:** every file's sha256 was checked first and matches J2562's.
- **Run record:** tmux `J2594-gate`, log `~/_desk/logs/J2594-gate.log`, exit file `~/_desk/logs/J2594-gate.done` (0), raw JSON `~/_desk/logs/J2594-results.json`; the like-for-like check on the three History of Science Shorts is `~/_desk/logs/J2594-side-results.json`.

## Result

**Result, plainly: the padding check came out on all thirteen as J2562 and the by-eye audit have them. The whole-Short verdict did not, on two of them, for a reason that is not the change under test. So by the brief's own wording ("all thirteen come out as J2562 had them") this is not a clean pass, and the job is parked for the Chief to rule.**

- **Padding check (what #817 changes):** the four full-frame Shorts are under both limits; all nine padded Shorts are over. `bSjWiCbB7pY` passes only through the list of cuts Ben OK'd before the rule (raw: 12 of 27 on the second with a straight edge, 24 of 53 padded-looking). No Short changed sides.
- **Two whole-Short verdicts differ from J2562: `cLKDiYP55J8` and `xgx2lYHhYZM` (both History of Science, both full frame) read FAIL.** The only failing line is `Orbit in frame at 0 s (visor 0.0060 / 0.0036 >= 0.003) — picture-first lock`. That is an Orbit With Ben rule. It fires because the brief had all thirteen run from the Orbit With Ben copy; J2562 ran History of Science Shorts from their own repo. Checked both ways: the same two Shorts get the same FAIL from the Orbit With Ben copy on `main` (`8ce0e9cb3726…`, before the change), and all three History of Science Shorts PASS from the History of Science copy of this change (history-of-science #513, `80bd45f7`; the gate file there is byte-identical, `f37031aeec42…`).
- **One new thing to look at: `f17XCtUmN-g` (full frame) has a between-seconds frame with a straight edge found, at 10.5 s.** It sits between the seconds, so the straight-edge count (one a second) does not read it: 0 of 21. It passes (2 of 42 padded-looking). But its warning now reads "does not fill 9:16" where J2562's read "may not fill ... no straight edge found". The grey frame is saved beside the report (the title card over the shot).

**The margin each way (padded-looking count, limit 15%)**

| Id | By-eye | J2562, one a second | Now, two a second |
|---|---|---|---|
| `Wvjd8g0CpzE` | full frame | 3 of 26 (11.5%); 3 allowed; the next padded-looking frame fails it | 5 of 51 (9.8%); 7 allowed; it can take 2 more and pass, the 3rd fails it |
| `kKN8Ale42sE` | padded | 4 of 21 (19.0%); 3 allowed; fails by 1 frame | 8 of 42 (19.0%); 6 allowed; fails by 2 frames |
| `xdurJQcoiGM` | padded | 4 of 19 (21.1%); 2 allowed; fails by 2 frames | 7 of 37 (18.9%); 5 allowed; fails by 2 frames |

Neither of the last two has a frame with a straight edge on the second, so both still fail on the 15% figure alone.

## Table: one row per Short

"Frames on the second" are the frames the straight-edge count reads (the same frames as J2562). "All frames" are two a second; the padded-looking count reads those. Both leave out an end card the cut's meta names (only `f17XCtUmN-g`, 20.92-22.36 s).

| # | Id | Ch | Airs | By-eye audit | Frames on the second | of those, padded with a straight edge | All frames (two a second) | of those, look padded | Padded stretches (as the gate prints them) | Whole Short | Rule that decides | Same verdict as J2562? | As the by-eye audit? |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---|---|---|
| 1 | `Wvjd8g0CpzE` | HOS | 2026-11-15 | full frame | 26 | 0 (0.0%) | 51 | 5 (9.8%) | 4.5-6.5 s (blur-pad, no edge), 7-7.5 s (blur-pad, no edge) | **PASS** | none: under both limits | yes (PASS) | yes |
| 2 | `f17XCtUmN-g` | OWB | 2026-12-16 | full frame | 21 | 0 (0.0%) | 42 | 2 (4.8%) | 10.5-11.5 s (blur-pad / blur-pad, no edge) | **PASS** | none: under both limits | yes (PASS) | yes |
| 3 | `cLKDiYP55J8` | HOS | 2026-11-13 | full frame | 23 | 0 (0.0%) | 45 | 2 (4.4%) | 9-10 s (blur-pad, no edge) | **FAIL under the Orbit copy; PASS under the History of Science copy** | not the padding check (under both limits): the Orbit-at-frame-0 lock, an Orbit With Ben rule | padding check yes; whole verdict NO under the Orbit copy (J2562: PASS) | padding check yes |
| 4 | `xgx2lYHhYZM` | HOS | 2026-11-17 | full frame | 25 | 0 (0.0%) | 49 | 1 (2.0%) | 14-14.5 s (blur-pad, no edge) | **FAIL under the Orbit copy; PASS under the History of Science copy** | not the padding check (under both limits): the Orbit-at-frame-0 lock, an Orbit With Ben rule | padding check yes; whole verdict NO under the Orbit copy (J2562: PASS) | padding check yes |
| 5 | `kKN8Ale42sE` | OWB | 2026-11-17 | padded | 21 | 0 (0.0%) | 42 | 8 (19.0%) | 5-9 s (blur-pad, no edge) | **FAIL** | all-padded rule (over 15%, two a second) | yes (FAIL) | yes |
| 6 | `xdurJQcoiGM` | OWB | 2026-11-25 | padded | 19 | 0 (0.0%) | 37 | 7 (18.9%) | 15-18.5 s (blur-pad, no edge) | **FAIL** | all-padded rule (over 15%, two a second) | yes (FAIL) | yes |
| 7 | `rvug71d7Dqk` | OWB | 2026-11-21 | padded | 23 | 9 (39.1%) | 45 | 25 (55.6%) | 3-3.5 s (blur-pad), 6.5-7 s (blur-pad), 11-22.5 s (blur-pad / blur-pad, no edge) | **FAIL** | edge rule (over 10%, one a second) and all-padded rule (over 15%, two a second) | yes (FAIL) | yes |
| 8 | `C8lPx5N2DwM` | OWB | 2026-12-05 | padded | 33 | 12 (36.4%) | 66 | 41 (62.1%) | 8.5-11.5 s (blur-pad), 14.5-32 s (blur-pad / blur-pad, no edge) | **FAIL** | edge rule (over 10%, one a second) and all-padded rule (over 15%, two a second) | yes (FAIL) | yes |
| 9 | `k2kEaA7ICjc` | OWB | 2026-12-11 | padded | 34 | 12 (35.3%) | 68 | 32 (47.1%) | 0-2.5 s (blur-pad / blur-pad, no edge), 12.5-19 s (blur-pad), 21.5-27 s (blur-pad), 32.5-34 s (blur-pad, no edge) | **FAIL** | edge rule (over 10%, one a second) and all-padded rule (over 15%, two a second) | yes (FAIL) | yes |
| 10 | `ffYKoNVPoqg` | OWB | 2026-11-10 | padded | 18 | 13 (72.2%) | 36 | 26 (72.2%) | 0-8 s (blur-pad), 13-18 s (blur-pad / mirror) | **FAIL** | edge rule (over 10%, one a second) and all-padded rule (over 15%, two a second) | yes (FAIL) | yes |
| 11 | `bSjWiCbB7pY` | OWB | 2026-11-13 | padded | 27 | 12 (44.4%) | 53 | 24 (45.3%) | 3-6 s (blur-pad), 10-19 s (blur-pad / mirror) | **PASS (raw rule FAIL; passes only by the OK'd-before-the-rule list)** | edge rule (over 10%, one a second) and all-padded rule (over 15%, two a second) | yes (PASS) | yes |
| 12 | `SWDCZfWZVao` | OWB | 2026-12-09 | padded | 23 | 6 (26.1%) | 46 | 18 (39.1%) | 3-5.5 s (blur-pad), 9-15.5 s (blur-pad / blur-pad, no edge) | **FAIL** | edge rule (over 10%, one a second) and all-padded rule (over 15%, two a second) | yes (FAIL) | yes |
| 13 | `heiGCnGKTkE` | OWB | 2026-12-14 | padded | 24 | 9 (37.5%) | 48 | 18 (37.5%) | 6-9 s (blur-pad), 12.5-16.5 s (blur-pad / mirror), 20-22 s (blur-pad) | **FAIL** | edge rule (over 10%, one a second) and all-padded rule (over 15%, two a second) | yes (FAIL) | yes |

## How close each Short is to the two limits

| Id | By-eye | Straight-edge frames / allowed, of frames on the second (10%) | Padded-looking frames / allowed, of all frames (15%) | Now | J2562: padded-looking / allowed, one a second |
|---|---|---|---|---|---|
| `Wvjd8g0CpzE` | full frame | 0 / 2 allowed of 26 | 5 / 7 allowed of 51 | passes; 3 more padded-looking frame(s) before a fail (fails at 8) | 3 / 3 allowed of 26 |
| `f17XCtUmN-g` | full frame | 0 / 2 allowed of 21 | 2 / 6 allowed of 42 | passes; 5 more padded-looking frame(s) before a fail (fails at 7) | 1 / 3 allowed of 21 |
| `cLKDiYP55J8` | full frame | 0 / 2 allowed of 23 | 2 / 6 allowed of 45 | passes; 5 more padded-looking frame(s) before a fail (fails at 7) | 1 / 3 allowed of 23 |
| `xgx2lYHhYZM` | full frame | 0 / 2 allowed of 25 | 1 / 7 allowed of 49 | passes; 7 more padded-looking frame(s) before a fail (fails at 8) | 1 / 3 allowed of 25 |
| `kKN8Ale42sE` | padded | 0 / 2 allowed of 21 | 8 / 6 allowed of 42 | fails; padded-looking count 2 over | 4 / 3 allowed of 21 |
| `xdurJQcoiGM` | padded | 0 / 1 allowed of 19 | 7 / 5 allowed of 37 | fails; padded-looking count 2 over | 4 / 2 allowed of 19 |
| `rvug71d7Dqk` | padded | 9 / 2 allowed of 23 | 25 / 6 allowed of 45 | fails; edge count 7 over; padded-looking count 19 over | 13 / 3 allowed of 23 |
| `C8lPx5N2DwM` | padded | 12 / 3 allowed of 33 | 41 / 9 allowed of 66 | fails; edge count 9 over; padded-looking count 32 over | 20 / 4 allowed of 33 |
| `k2kEaA7ICjc` | padded | 12 / 3 allowed of 34 | 32 / 10 allowed of 68 | fails; edge count 9 over; padded-looking count 22 over | 15 / 5 allowed of 34 |
| `ffYKoNVPoqg` | padded | 13 / 1 allowed of 18 | 26 / 5 allowed of 36 | fails; edge count 12 over; padded-looking count 21 over | 13 / 2 allowed of 18 |
| `bSjWiCbB7pY` | padded | 12 / 2 allowed of 27 | 24 / 7 allowed of 53 | fails; edge count 10 over; padded-looking count 17 over | 12 / 4 allowed of 27 |
| `SWDCZfWZVao` | padded | 6 / 2 allowed of 23 | 18 / 6 allowed of 46 | fails; edge count 4 over; padded-looking count 12 over | 10 / 3 allowed of 23 |
| `heiGCnGKTkE` | padded | 9 / 2 allowed of 24 | 18 / 7 allowed of 48 | fails; edge count 7 over; padded-looking count 11 over | 9 / 3 allowed of 24 |

## The gate's own lines on the padding check

- `Wvjd8g0CpzE` (HOS, sha256 `e1f862ba737a…`, same file as J2562: yes; exit 0, 7.9 s) — PASS
  - the picture may not fill 9:16 on 5/51 sampled frames: 4-6s (blur-pad, no edge), 7-8s (blur-pad, no edge). They are soft above and below a detailed middle, with no straight edge found, so this is not a FAIL: look at those seconds and say which it is
- `f17XCtUmN-g` (OWB, sha256 `344bd0d0ab04…`, same file as J2562: yes; exit 0, 9.2 s) — PASS
  - the picture does not fill 9:16 on 2/42 sampled frames: 10-12s (blur-pad / blur-pad, no edge)
- `cLKDiYP55J8` (HOS, sha256 `3ef3fa773750…`, same file as J2562: yes; exit 1, 7.6 s) — FAIL
  - the picture may not fill 9:16 on 2/45 sampled frames: 9-10s (blur-pad, no edge). They are soft above and below a detailed middle, with no straight edge found, so this is not a FAIL: look at those seconds and say which it is
- `xgx2lYHhYZM` (HOS, sha256 `e5ea76f012fb…`, same file as J2562: yes; exit 1, 8.4 s) — FAIL
  - the picture may not fill 9:16 on 1/49 sampled frames: 14-14s (blur-pad, no edge). They are soft above and below a detailed middle, with no straight edge found, so this is not a FAIL: look at those seconds and say which it is
- `kKN8Ale42sE` (OWB, sha256 `b8bb56f7ef66…`, same file as J2562: yes; exit 1, 13.7 s) — FAIL
  - the picture does not fill 9:16 on 8/42 frames sampled twice a second (19.0%; 0 with a straight edge at the picture; limit 15% when no edge is found): 5-9s (blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- `xdurJQcoiGM` (OWB, sha256 `74aa35464bf2…`, same file as J2562: yes; exit 1, 12.6 s) — FAIL
  - the picture does not fill 9:16 on 7/37 frames sampled twice a second (18.9%; 0 with a straight edge at the picture; limit 15% when no edge is found): 15-18s (blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- `rvug71d7Dqk` (OWB, sha256 `06b935f706c8…`, same file as J2562: yes; exit 1, 6.0 s) — FAIL
  - the picture does not fill 9:16 on 13/23 frames sampled once a second (57%, limit 10%): 3-4s (blur-pad), 6-7s (blur-pad), 11-22s (blur-pad / blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- `C8lPx5N2DwM` (OWB, sha256 `ebe11bb730cc…`, same file as J2562: yes; exit 1, 10.4 s) — FAIL
  - the picture does not fill 9:16 on 20/33 frames sampled once a second (61%, limit 10%): 8-12s (blur-pad), 14-32s (blur-pad / blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- `k2kEaA7ICjc` (OWB, sha256 `ff4194857a02…`, same file as J2562: yes; exit 1, 10.2 s) — FAIL
  - frame 0 is not full-bleed 9:16: blur-pad above and below a picture band on 2/3 frames from 0.0 to 0.5 s (at 0.25s, sharp pixels above/middle/below 0%/8%/3%: no fine detail above or below, yet a picture's brightness is there) — reframe the opening shot to fill 1080x1920
  - the picture does not fill 9:16 on 15/34 frames sampled once a second (44%, limit 10%): 0-2s (blur-pad / blur-pad, no edge), 12-19s (blur-pad), 22-27s (blur-pad), 32-34s (blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- `ffYKoNVPoqg` (OWB, sha256 `8eead2f62fd3…`, same file as J2562: yes; exit 1, 11.4 s) — FAIL
  - frame 0 is not full-bleed 9:16: blur-pad above and below a picture band on 3/3 frames from 0.0 to 0.5 s (at 0.00s, sharp pixels above/middle/below 0%/73%/2%: no fine detail above or below, yet a picture's brightness is there) — reframe the opening shot to fill 1080x1920
  - the picture does not fill 9:16 on 13/18 frames sampled once a second (72%, limit 10%): 0-8s (blur-pad), 13-18s (blur-pad / mirror) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- `bSjWiCbB7pY` (OWB, sha256 `54929328bd18…`, same file as J2562: yes; exit 0, 13.5 s) — PASS (raw rule FAIL; passes only by the OK'd-before-the-rule list)
  - the picture does not fill 9:16 on 12/27 frames sampled once a second (44%, limit 10%): 3-6s (blur-pad), 10-19s (blur-pad / mirror) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band) [not a FAIL for this file: OK'd before the rule (Ben, 10 Nov 2026 16:22Z, on the board; asked in J2510); a re-cut is not covered]
- `SWDCZfWZVao` (OWB, sha256 `e0459b017dda…`, same file as J2562: yes; exit 1, 10.9 s) — FAIL
  - the picture does not fill 9:16 on 10/23 frames sampled once a second (43%, limit 10%): 3-6s (blur-pad), 9-16s (blur-pad / blur-pad, no edge) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)
- `heiGCnGKTkE` (OWB, sha256 `31f362f4437b…`, same file as J2562: yes; exit 1, 9.6 s) — FAIL
  - the picture does not fill 9:16 on 9/24 frames sampled once a second (38%, limit 10%): 6-9s (blur-pad), 12-16s (blur-pad / mirror), 20-22s (blur-pad) — make every shot fill 1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)

## The two History of Science Shorts, three ways

| Id | Orbit With Ben copy, this branch (`67cb29f5`) | Orbit With Ben copy, `main` (before the change) | History of Science copy, #513 (`80bd45f7`) |
|---|---|---|---|
| `Wvjd8g0CpzE` | PASS | PASS | PASS |
| `cLKDiYP55J8` | FAIL: Orbit in frame at 0 s (visor 0.0060) | FAIL: the same line | PASS |
| `xgx2lYHhYZM` | FAIL: Orbit in frame at 0 s (visor 0.0036) | FAIL: the same line | PASS |

The padded frames are the same in the branch copy and the History of Science copy (5 of 51, 2 of 45, 1 of 49).

## Frames saved (grey, 108 x 192)

- `cLKDiYP55J8_0.0s_grey.png`, `xgx2lYHhYZM_0.0s_grey.png`: frame 0 of the two Shorts the Orbit lock trips on. No padded frame changed sides on either.
- `f17XCtUmN-g_10.5s_grey.png`: the between-seconds frame where a straight edge was found.

## What was not done

- No figure was touched, and no ruling made: whether the two Orbit-lock verdicts count against the pass condition is the Chief's call.
- Nobody watched the Shorts in this job. The by-eye column is J2545's audit; this job ran the check and counted.
- **The History of Science desk post was not made.** `hos_desk.py post --from` accepts only claude, grok, cursor, codex, ben and gemini; a worker posting under one of those would put its words under another agent's id. The text is in `DESK_POST.md` beside this report: `hos_desk.py post --from <own id> --to grok --stage tooling --status review --body-file <that file>`.
