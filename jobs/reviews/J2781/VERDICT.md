# J2781: Rule-E topic go/no-go, OWB 066 and 067

- **Reviewer:** `macbook` (Claude Code on the MacBook, review lane), 13 Nov 2026
- **Reviewed:** the two `TOPIC.md` files on branch `macbook/J2778` at `96a6751ca` (PR #901, open, base `main`)
- **Against:** `AGENTS.md` rule E, `STUDIO_PLAYBOOK.md` §2, `05_Analytics/LEARNINGS.md` rules 1-31 and OWB-2026-11-E1, `studio/RULES.md`

| Film | Verdict |
|---|---|
| **OWB:066** Why Do We Only See One Side of the Moon? (The Hidden Far Side) | **GO**, with the fix list below carried into the script job |
| **OWB:067** What Would Happen If You Fell Into Neptune? (2,000 km/h Winds) | **GO**, with the fix list below carried into the script job |

Both stay in `jobs/WIP.json` `next` (rule G). This review queues nothing: their production starts when an Orbit place frees up. PR #901 itself is the Chief's to merge.

## What I could and could not check

- **Checked here:** the two briefs in full (section 2 of each), the repo for overlap (`02_Video-Projects/`, `VIDEO_BACKLOG.json`, the 013 scripts, every public title in `05_Analytics/owb/snapshots/2026-11-13.json`), the briefs' own arithmetic and whether each spoken claim has a quote in the brief's fact base.
- **Not re-checked:** the neighbours' view counts, the "0 exact title collisions" searches, the search suggestions and the NASA quotes. This worker has no web access. They are taken as J2778 recorded them, and the Gemini claims pass at script stage re-checks every quote against its page as usual.

## Rule E rubric

| Rubric item | 066 Moon | 067 Neptune |
|---|---|---|
| 1. No near-duplicate of a live or scheduled video | **PASS.** The only Moon long is 013 (`2fsQcea-voM`, the Moon drifting away). Its four script files never mention tidal locking, the same face or the far side (grep: 0 hits). The six public Moon Shorts are all about the 3.8 cm drift. | **PASS, with two packaging overlaps to fix (N1, N2).** No Neptune long exists; 035 is Triton. The Jupiter descent (`-jmMROGoZCM`) is the same kind of film on a different planet, which rule 20's "What Would Happen If…" series expects. |
| 2. Audience evidence | **PASS.** Rule 26 phrase and two ranking videos named. Five neighbours recorded over 1.8M (playbook §2 needs three near 1M). | **PASS.** Rule 26 phrase and two ranking videos named. Seven neighbours recorded over 1.48M. Own data: the Neptune winds Short `1OCNzhkiBuc` is one of our best on stayed-to-watch (LEARNINGS rules 8 and 24). |
| 3. Numbers have a sourced fact | **PASS for a topic; three claims lack a quote (M2).** | **PASS for a topic; diamond rain and Mach 1.7 lack any source (N3, N4), and one figure contradicts itself (N5).** |

## Fix list for 066 (script and packaging jobs; none blocks the go)

- **M1. The first line is too long.** The brief's cold-open sentence is about 55 words, roughly 20 s spoken. `studio/RULES.md` (first 30 seconds of a long, rule 2) wants the first line to end before 0:08. Split it: the same-face claim first, then the 27-day lock, then the crust.
- **M2. Three things said in the brief have no quote in its fact base (§2.5).** "Luna 3" (the NASA quote says only "a Soviet spacecraft … in 1959"), Apollo 8 in 1968, and "NASA gravity maps revealed why" (GRAIL). Each needs its own `SOURCES.md` row with a quote and link, or it is cut.
- **M3. The crust explanation is stated as settled.** NASA's quoted text gives the two thicknesses (about 40 km and up to about 60 km) and when the maria filled. It does not say the thicker crust is why the far side has few maria. Say it as the leading explanation unless a source row says more. Short S02's payoff has the same wording.
- **M4. Shorts are under the length floor.** S01 is planned at 19-21 s and S02 at 20-22 s. The Keeper score floor is 22 s for every new Short (the ~20 s exception belongs to the J0216 test only and ends 20 Nov 2026), and E1 keeps the Keeper length rule. Plan both at 22-27 s, 55-65 words.
- **M5. Rule 31 is quoted as proven.** The brief says ground-visible topics "proved" a 10-50x advantage. LEARNINGS rule 31 calls it "a hunch to test, not a finding" on two Shorts. It is a fair reason to pick the topic, not evidence of the size of the effect.
- **M6. Neighbour 5 is weak.** The Cosmicus video is a sensational-title channel, not a clear education neighbour. The pool still passes on the other four (2.07M to 4.21M); do not take subject words or framing from it ("terrifying" is fear framing, on the Never list).

## Fix list for 067 (script and packaging jobs; none blocks the go)

- **N1. Title B copies our own live Short.** "Why Are Neptune's Winds Faster Than Sound?" is the public Short `1OCNzhkiBuc` "Why Are the Winds on Neptune Faster Than Sound?" reworded. Drop it as a long title variant.
- **N2. Short S01 repeats that live Short's idea.** Its overlay is "2,000 KM/H WINDS" and its payoff leads on the winds. "Re-upload an idea that already went public" is on the Never list. Keep the title and frame 0 (no ground), and make the single fact the descent with no surface (atmosphere merging into hot dense fluid), with a different overlay.
- **N3. Diamond rain has no source at all.** It is in the cold open, title D, thumb B ("RAINS DIAMONDS"), and the whole of Short S02, with "millions of bars" and "sink like hailstones". None of it is in the two NASA pages quoted in §2.5, so the brief's "0 unverified numbers" is not true for it. Before script lock it needs a primary source row (a paper or lab press release with an exact quote), and the wording must match what that source supports: it is something experiments and models predict, not something observed. Without a source it is cut from the film and S02 is replaced.
- **N4. "Mach 1.7" has no source.** Thumb C says "MACH 1.7 WINDS". NASA's quote says "supersonic" and gives the speed; no speed of sound on Neptune is quoted. Use "SUPERSONIC" or the 2,000 km/h figure unless a source row gives the Mach number.
- **N5. The wind comparison contradicts itself on one graphic.** DATA 1 shows 2,000 km/h against Earth's 400 km/h, which is 5 times, beside "9x stronger than Earth's". Both numbers are NASA's, but NASA's "nine times stronger" is not a ratio of those two speeds. Put one comparison on the graphic. Short S01's "nine times faster than Earth's strongest hurricanes" is a paraphrase NASA does not make: quote "nine times stronger than Earth's" or use the speeds.
- **N6. The cold open puts the viewer in a storm that is gone.** "Hurl you across a storm as wide as the Earth": NASA's quote says the 1989 Great Dark Spot "has since disappeared". Say it in the past, or as "storms like the one Voyager 2 saw".
- **N7. The first line is too long.** About 60 words in one sentence; the first line must end before 0:08. Also "three billion miles" against NASA's 2.8 billion: say "nearly three billion".
- **N8. Title C overclaims.** "What Voyager 2 Saw Inside Neptune's Giant Dark Storm": Voyager 2 flew past and did not see inside the storm. Rule 18 allows a real-imagery title only where the sources prove it. Reword ("What Voyager 2 Saw at Neptune") or drop.
- **N9. The main title sits close to two public titles.** "What If You Fell Into Neptune?" (`vC8fZSStdJQ`) and "What Would You See If You Fell Into Neptune?" (`B0v7MihXA-s`). It is not a copy, and the bracketed tail sets it apart, so it passes; the Chief's title check before upload should look at it once more. Playbook §2 step 3 (are the top five results all very large channels?) is not recorded in the brief: the film's own angle (the real Voyager 2 picture and NASA numbers, step by step down) is the narrowing, and the script should hold to it.
- **N10. Shorts are under the length floor.** Both are planned at 19-21 s. Same as M4: 22-27 s, 55-65 words.

## For the Chief

- No protected call is made here. A rule-E topic verdict is the review lane's (rule E); merging PR #901 is the Chief's.
- When either film enters `active`, its script job brief should carry this fix list, and the diamond-rain source (N3) is the one item that can change 067's content.
