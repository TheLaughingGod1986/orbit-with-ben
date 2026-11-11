Claude Code covering — J2594: the thirteen real Shorts rerun with the twice-a-second count (branch of #817, commit `67cb29f531`, the Orbit With Ben copy for all thirteen; every file's sha256 matches J2562). Read-only, no spend.

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

Full report, the gate's own lines and three grey frames: `jobs/reviews/J2594/` (pull request below). Nobody watched the Shorts in this job; the by-eye column is J2545's audit.
