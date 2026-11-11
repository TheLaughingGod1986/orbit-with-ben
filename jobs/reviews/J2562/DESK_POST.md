Claude Code covering J2562 (worker, Mac mini): the new Shorts check (straight-edge evidence, orbit-with-ben #794 / history-of-science #502) run read-only on the thirteen Shorts you asked for. Report: orbit-with-ben pull request #809, `jobs/reviews/J2562/REPORT.md`. Parked for the Chief.

**All thirteen came out as expected. None of the nine padded Shorts stopped failing.**

Frames are sampled once a second. Limits: 10% padded with a straight edge, 15% padded-looking with or without one.

| Id | Ch | By eye | Sampled | Padded, edge | Padded, no edge | Padded stretches | Whole Short | Opening |
|---|---|---|---:|---:|---:|---|---|---|
| `Wvjd8g0CpzE` | HOS | full | 26 | 0 | 3 | 5-8 s (no edge) | PASS, warning | PASS |
| `f17XCtUmN-g` | OWB | full | 21 | 0 | 1 | 11-12 s (no edge) | PASS, warning | PASS |
| `cLKDiYP55J8` | HOS | full | 23 | 0 | 1 | 9-10 s (no edge) | PASS, warning | PASS |
| `xgx2lYHhYZM` | HOS | full | 25 | 0 | 1 | 14-15 s (no edge) | PASS, warning | PASS |
| `kKN8Ale42sE` | OWB | padded | 21 | 0 | 4 | 5-9 s (no edge) | FAIL (19.0%, 15% rule) | PASS |
| `xdurJQcoiGM` | OWB | padded | 19 | 0 | 4 | 15-19 s (no edge) | FAIL (21.1%, 15% rule) | PASS |
| `rvug71d7Dqk` | OWB | padded | 23 | 9 | 4 | 3-4 s, 11-23 s | FAIL (57%) | PASS |
| `C8lPx5N2DwM` | OWB | padded | 33 | 12 | 8 | 9-12 s, 15-32 s | FAIL (61%) | PASS |
| `k2kEaA7ICjc` | OWB | padded | 34 | 12 | 3 | 0-3 s, 13-19 s, 22-27 s, 33-34 s | FAIL (44%) | FAIL |
| `ffYKoNVPoqg` | OWB | padded | 18 | 13 | 0 | 0-8 s, 13-18 s | FAIL (72%) | FAIL |
| `bSjWiCbB7pY` | OWB | padded | 27 | 12 | 0 | 3-6 s, 10-19 s | PASS only by the OK'd-before-the-rule list; raw 44.4%, all 12 with an edge, fails the 10% rule | PASS |
| `SWDCZfWZVao` | OWB | padded | 23 | 6 | 4 | 3-6 s, 9-16 s | FAIL (43%) | PASS |
| `heiGCnGKTkE` | OWB | padded | 24 | 9 | 0 | 6-9 s, 13-17 s, 20-22 s | FAIL (38%) | PASS |

Two things to weigh on the 15% figure:

1. `kKN8Ale42sE` and `xdurJQcoiGM` have no straight edge found on any frame (feathered blur). They fail on the 15% figure alone, by one frame and by two.
2. `Wvjd8g0CpzE` passes with 3 padded-looking frames of 26, and 3 is the most it may have. One more soft frame and it fails again.

So the figure separates the two groups on these thirteen, with one sampled frame of room each way. No change was made to the gate or its numbers. Nobody watched the Shorts in this job; the by-eye column is the J2545 audit.

The History of Science Shorts were run from a clean copy of history-of-science main (1fb86005), whose gate file is byte-identical to orbit-with-ben's. The shared History of Science checkout on the Mini is on another branch with the older gate; I left it alone.
