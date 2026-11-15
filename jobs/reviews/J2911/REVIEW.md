# J2911 — Rule-E topic go/no-go: OWB 068 (Mercury day) and OWB 069 (Rosetta comet landing)

- **Reviewer:** `macbook-2` (Claude Code, MacBook slot 2), 15 Nov 2026
- **Reviewed:** `02_Video-Projects/068_How-Long-Is-A-Day-On-Mercury/TOPIC.md` and `02_Video-Projects/069_Landing-On-A-Comet-Rosetta-67P/TOPIC.md` at commit `b24f599ee`, with each film's `11_Upload-Package/evidence_2026-11-15_public_search.json` and `evidence_2026-11-15_neighbours.json`, against `AGENTS.md` rule E, `studio/RULES.md` (neighbour pass, Never list), `studio/plan.json` and `jobs/WIP.json`.
- **Spend:** none. Nothing on YouTube was read or changed.
- **Limit of this review:** this lane has no web search, so nothing was re-pulled from YouTube. Every view count below is judged only by whether it is in the saved evidence files. The science was checked from the cited papers and fact sheets as I know them, not re-fetched; items I could not confirm are marked "check at SOURCES".

## Verdicts

| Film | Verdict | In one line |
|---|---|---|
| **OWB:068** Mercury day | **GO as a topic, FIX before a script job is queued** | No duplicate, real audience evidence (our own Short), core numbers sourced. Two Short lines are wrong and five of the eight neighbours are not in the saved evidence. |
| **OWB:069** Rosetta comet landing | **GO as a topic, FIX before a script job is queued** | No duplicate, four on-topic videos over 1M in the saved evidence, core paper numbers hold. The cold-open hook and Short S01 are factually wrong and must be rewritten. |

Neither GO starts any work. Both films stay where they are in `jobs/WIP.json` `next` (places 29 and 30), and both are single-question longs, which `studio/plan.json` pauses after the Pluto film on 13 Dec until a format test has its result. So no script job is queued from this review.

## Rule-E rubric

| Check | 068 | 069 |
|---|---|---|
| 1. No near-duplicate of a live or scheduled video | **PASS.** The only live Mercury video is our Short `vlkj8RQKmH8`, which this long would parent. `036` (ice on Mercury) and `061` (Venus day longer than its year) are different subjects, both unbuilt. | **PASS.** The only live comet video is the Short *Why Will Gliese 710's Comets Arrive After It Has Gone?*, a different subject. No film or idea covers Rosetta, Philae or 67P. |
| 2. Audience evidence | **PASS on our own data.** `vlkj8RQKmH8`: 851 views, 76% average viewed. Autocomplete returns the exact phrase. See FIX 3 and 4: the search evidence is weaker than the brief says. | **PASS.** In the saved search file: 2,757,055 and 829,635 views rank for "landing on a comet"; 2,666,471, 1,689,644 and 1,180,863 rank for "why do comets have tails". |
| 3. Every number has a sourced fact | **PASS for the long's core numbers** (87.969 d, 58.6462 d, 175.94 d, 0.2056, 1965 radar result). **FAIL on two Short lines** (FIX 1, 2). Tour numbers have no source rows yet. | **PASS for the paper numbers** (touchdown times, 1 h 50 min bounce, 4.3 × 2.6 × 2.1 km, 533 kg/m³, D/H 5.3 × 10⁻⁴). **FAIL on the hook and Short S01** (FIX 1, 2). |

## OWB:068 — FIX list

1. **Short S02 title is false.** *"Why Is Mercury's Night Cold Enough to Freeze Nitrogen?"* Nitrogen freezes at about −210 °C and boils at about −196 °C. A −180 °C night does not even liquefy it. Retitle from the line the Short actually says, for example *Why Is the Planet Closest to the Sun So Cold at Night?* Also fix its heading, which says "How Arecibo Radar Broke the 88-Day Myth" over a script about the cold night.
2. **Short S01 gives the wrong speed.** It says the orbit swings Mercury to 46 million km from the Sun, "accelerating the planet to forty-seven kilometres per second". 47.36 km/s is the fact sheet's mean orbital speed. At perihelion Mercury moves at about 59 km/s. Use the perihelion figure with its own source row, or drop the number. The `47 KM/S ORBIT SPEED` overlay goes with it.
3. **The "search gap" claim is contradicted by the brief's own evidence file.** The brief says there is "zero modern 8–10 minute documentary" on the phrase. `evidence_2026-11-15_public_search.json` lists six recent films of 6:43 to 10:04 on exactly this question, with 3, 5, 7, 45, 120 and 134 views, and a 3:45 one with 394. The gap is not empty: small channels are filling it and getting almost nothing. Say so in the brief. It is the strongest argument against the single-subject version and for waiting on the format tests.
4. **Five of the eight "verified" neighbours are not in either saved evidence file:** the 10,371,299, 4,078,021, 2,843,899, 2,054,895 and 1,712,203 rows. Of the three that are: one is a logic riddle that is not about Mercury (4,751,236; its saved length is 6:01, the table says 4:56), one is a 25-second Short about the length of a year (3,755,128), and one is a real neighbour (1,675,186; saved length 10:18, table 10:36). The `neighbours.py` PASS counted off-topic results ("How do solar panels work?", an Earth-orbit talk). Re-pull the five by video id into the evidence file and take the riddle out of the table. Until then the saved evidence shows one on-topic long over 1M, not eight.
5. **The eight-planet tour recast overlaps `064` *Every Planet Explained in 10 Minutes*,** which is the plan's own test film and still waits on Ben's lock. A second all-planets tour is not approved by the plan. Keep the recast as a note only; whether more tours get made is decided after 064's test (keep 500 views, drop 230, 14 days), in `studio/plan.json`, by the Chief. If it is ever built, each tour number needs a `SOURCES.md` row: check the 640 km/h Jupiter jets and the "+1.78 ms/century" figure, and drop "frictionless" for Neptune's clouds.
6. **Minor:** Short S01's title is 50 characters, not 54.

## OWB:069 — FIX list

1. **The cold-open hook is wrong in three ways and cannot be used.** *"…real camera footage shot from the surface of a four-kilometre comet hurtling toward the Sun at one hundred and thirty-five thousand kilometres per hour."*
   - The 1 June 2016 OSIRIS sequence was taken by the Rosetta orbiter about 13 km from the comet (the brief says so itself two lines later), not from the surface.
   - In June 2016 the comet was ten months past its closest approach to the Sun (August 2015) and heading away from it.
   - 135,000 km/h is the comet's top speed near the Sun. Out at about 3 AU in June 2016 it was moving at roughly half that. Check at SOURCES and use a figure for the date shown, or no speed.
2. **Short S01 repeats all three errors and overstates the "snowstorm".** ESA's own note on that sequence says most of the streaks are background stars and dust grains close to the camera, with cosmic-ray hits. "Sunlight boiling buried ice blasted boulders and dust off kilometre-high cliffs into a swirling cosmic blizzard" is not what the images show. Rewrite S01 from what ESA says is in the frame, and soften `SNOW ON A COMET` and `REAL COMET FOOTAGE` to match. The sequence is 25 minutes of still images, so "footage" in the long's title needs the description to say so.
3. **The gravity figure is inconsistent.** The brief gives `~10⁻³ m/s²` beside "100,000× weaker than Earth" and "100 kg weighed about 1 gram". The last two need about 10⁻⁴ m/s². Fix the number and give it a source row.
4. **Neighbour table.** Two rows are not in the saved evidence (1,776,300 and 1,012,609). The 7,947,482 row is a talk about an interstellar object, not comets or Rosetta, and its saved length is 13:25, not 15:24. Four on-topic videos over 1M are in the saved files, so the pass stands; correct the table. The `neighbours.py` PASS here also counted Rosetta Stone and solar-panel videos.
5. **The tour recast title does not hold up.** *"Every World Humans Have Landed On in 10 Minutes (7 Real Landings)"*: no human has landed on six of the seven; three asteroids are folded into one "world" to make the count; Bennu and Ryugu were touch-and-go sampling; and "every" is easy to disprove. As with 068, a new tour is the plan's call after 064's test, not this brief's.
6. **Image licence, check at SOURCES.** The brief calls the OSIRIS archive "CC BY-SA 3.0 IGO / public educational release". "Public educational release" is not a licence, and I believe OSIRIS images are CC BY-SA 4.0 with a long required credit line. Share-alike on the film's pictures is a Chief call before any shot list.
7. **Minor:** the first touchdown was followed by a brush with a crater rim before the second touchdown at 17:25:26 UTC; the brief merges the two.

## What happens next

- Both films stay in `jobs/WIP.json` `next`. No stage is queued.
- The FIX lists are for whoever next edits the two `TOPIC.md` files (a Mini lane with search, for the neighbour re-pulls). They must be done before either film's script job is queued.
- Commands this lane could not run (`jobs.py` is refused in the MacBook's unattended Claude Code):

```
python3 scripts/jobs.py done J2911 --agent macbook-2 --result "Rule-E review: 068 GO with 6 fixes, 069 GO with 7 fixes, both before any script job; both stay in WIP next (single-question pause). jobs/reviews/J2911/REVIEW.md" --git
```
