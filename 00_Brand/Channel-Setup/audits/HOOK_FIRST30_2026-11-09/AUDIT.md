# First 30 seconds audit (J2428, macbook-2, 9 Nov 2026)

Data: `05_Analytics/owb/REPORT.md`, *Where viewers leave*. Still watching at 0:30, with YouTube rating every one "lower" than similar videos: Venus 51%, Saturn rings 33%, Red dwarf 42%, JWST 66%, Alien worlds 48%, Fermi 39%.

## What the six openings share (script lines read)

| Film | Opening (VO) | Problem |
|---|---|---|
| 023 Venus | "Venus is the planet most like Earth. So what happened to it?" … "In this film, I will show you how that can be true, where its water went…" | Good line 1; agenda line at about 0:25 where the payoff should be |
| 021 Saturn rings | "Look along the sheet. It is not a solid disc. It is a crowd…" … "How long that takes is the question we are saving for the rain." | Scene-setting and ring physics first; the title's question (how long is left) is held back. Worst film: 33% |
| 004 JWST | "What if the universe was already busy…? Today, Orbit is going to learn beside the James Webb Space Telescope… This is JWST Discoveries the Orbit Way." | Series intro and mission statement; first concrete fact well after 0:30 |
| 003 Alien worlds | "Today, Orbit is going on a tour… This is exoplanets explained the Orbit way" | Series intro; questions instead of a real world at frame 0 |
| 001 Fermi | "Look up on a clear night… So where is everybody?… I'm Orbit — and today we're asking…" | Self-intro and restated question; no stakes or answer |
| 005 Red dwarf | no script in git | not read |

Shared pattern: a channel/series/Orbit intro or an agenda line, scene-setting before the question, the title's promise held back, the most striking real image late. The rule this produced is in `AGENTS.md`, *First 30 seconds (J2428)*.

## 032 / 033 / 034 against the rule (scripts read, picture NOT re-cut in this job)

- **032 Titan (v02):** line 1 is the title's question with stakes ("would you survive?"), agenda line already cut on 29 Oct. Payoff hint ("pressure would not hurt you… the cold would") lands in the opening paragraph. Script PASSes 2–4; the cut needs a frame-0 check (real Huygens/Cassini Titan plate) and ≤4 s cuts to 0:30.
- **033 Uranus (v02):** line 1 runs long ("At the north pole of Uranus, the seventh planet in orbit around our Sun, what would you see…"). The stakes ("a single winter night that lasts twenty-one Earth years") land near 8 s. Suggested trim with no re-voice: cut the clause "the seventh planet in orbit around our Sun" from the VO edit if the breath allows; otherwise this is the one sentence worth re-voicing. The shot list says "cut every four to six seconds": tighten to ≤4 s for the first 30 s.
- **034 Pluto (v03):** same long line-1 shape ("Across Pluto's horizon, in distant orbit around our Sun, what would you see…"); the stakes ("zero craters") come at the end of that sentence, past 8 s. Same trim: drop "in distant orbit around our Sun" in the edit, or re-voice line 1 with the usual VO checks. Sentence 2 is one very long number-heavy line; the payoff ("an active glacier") is there by about 0:20 only if the trim is made.

## Uploaded, not yet aired (026 / 027 / 031)

Not checked in this run (time cap). Each could take a re-cut opening only if the re-upload or replace keeps its `publishAt`; any change to a scheduled video is a YouTube state change and needs Chief's OK and a thread line (lesson 6). Left for a follow-up job.

## Not done in this job

- Re-cutting the 032/033/034 openings (needs the NAS working media and a render; over the 25-minute MacBook run).
- Mirroring the rule into the build rule file via `sync_rules` (the run could not execute Python).
