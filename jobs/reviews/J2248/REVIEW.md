# J2248 review: 024 muons Short `fri06_muons_ground` v01

**Verdict: FIX**

Reviewer: Claude on the MacBook (`macbook-2`), job J2250, 5 Nov 2026.
Not scheduled, not uploaded, no watch card set. £0.

## What I reviewed, and what I couldn't

- Reviewed: `fri06_muons_ground_v01_meta.json` (spoken line, captions with timings, title, hook, long),
  `cuts_v01.json`, `picture_qa_v01/picture_qa.json`, `polish_gate_v01.txt`, and the gate, sfx and music reports
  listed in the brief. Measured against AGENTS.md (lesson 5 Keeper score, *Teach on screen*), the
  `.cursor/rules/orbit-build-shorts.mdc` Keeper score and Learnings checklist, and lessons R7.
- **Not reviewed: the picture itself.** The iCloud copies in `OWB UAT/024_fri06_muons_ground_v01/`
  (mp4, contact sheet, cover) haven't downloaded to this MacBook. Reads fail with EDEADLK, and this
  unattended run couldn't call ffmpeg or shasum, so I didn't confirm the sha256 either. The verdict below comes
  from the rules alone; whoever reviews v02 still needs to watch the frames, including the s02 WARN.

The tool gates do PASS as the brief says. The FIX is for house rules that the gates don't check.

## Why FIX

1. **The whole Short is code graphics back to back (7 of 7 rows).** `cuts_v01.json` cuts
   `code_graphic_024_fri06_muons_s01` through `s07` end to end, with no real moving picture anywhere. The
   pool gives every row the same title, *"Our own cosmic-ray muon shower, cyan streaks already falling"*.
   That breaks *Teach on screen*: "never two code graphics back to back anywhere in the film, with real moving
   imagery between them", plus review gate item 6, MOTION. It also breaks the Shorts overlay rule: "at most one
   overlay". picture_qa doesn't count runs of graphics, which is why it passed. This is also the likely cause
   of the s02 low-detail WARN.
2. **The title is a statement, not a question (Keeper score 1–2).** *"Muons Shouldn't Reach the Ground. They
   Do."* is the statement-and-teaser shape that the rules call out (*Saturn's Rings Are on a Clock*, 12 views).
   Line 1, *"Particles from space are passing through you."*, is also a statement. This isn't the long's opening,
   so the Test A exemption doesn't apply, and the provisional 21 Nov air date is after the J0216 test ends.
3. **The spoken end title doesn't match the listing title (R7).** The VO and captions say *"What Happens If
   You Travel Near **The Speed Of Light**?"*, but the long `rVqgtkBV3jc` is listed as *"What Happens If You
   Travel Near **Light Speed**?"* (the meta's own `long.title`).
4. **"The full film" line runs to the loop seam (Keeper loop rule 4).** It is spoken from 16.9 s to 21.17 s
   of a 22.2 s cut. The rule allows no end card, CTA or "the full film" line in the last 2 s. The last line
   also doesn't run back into line 1 as one sentence.
5. **The answer lands inside the 9–14 s promo banner (Learnings #6).** "their clocks run slow" is spoken at
   13.02–14.74 s. The payoff starts at about 59% of runtime, not 70% (15.5 s) or later.
6. **There's a 0.68 s pause at the 4–5 s seam (Learnings #7).** "here" ends at 4.14 s and "Muons" starts at
   4.82 s. The rule allows a breath under 0.25 s and never a 0.5 s pause. There's another 0.52 s gap at
   11.32 → 11.84 s.
7. **The subject isn't named in 0–2.5 s (Learnings #2).** "Muons" is first said at 4.82 s.
8. Minor: the captions spell "meters". The house is British, so captions should read "metres".

## Exact changes for v02

- **Picture:** keep **one** code graphic, the slow-clock or 600 m vs ground scale bar, timed to its line.
  Rebuild the rest on real moving picture: a cosmic-ray or aurora sky plate from NASA or ESA, Earth from
  orbit, atmosphere or ground. Use real moving imagery between any graphics and change the picture every
  2.5–4 s. Then rerun picture_qa and polish_gate, and view the s02 replacement at full size.
- **Title and line 1:** one question in a keeper shape, for example *"Why Do Muons Reach the Ground?"* or
  *"How Do Muons Survive the Fall to Earth?"*. Line 1 asks it and says "muons" by 2.5 s.
- **VO (needs a new take, so ElevenLabs credit and Chief's OK):** cut the "The full film…" tail. Bridge
  into the 2-microsecond number with a breath under 0.25 s. Hold "clocks run slow, so they reach the ground"
  until 15.5 s or later, after the banner clears. Write the last line so it reads straight back into line 1.
  Keep 22–24 s and 55–65 words.
- **End:** the R7 card shows the exact listing title *"What Happens If You Travel Near Light Speed?"* and
  links `rVqgtkBV3jc`, and it sits before the loop seam. The last frame matches frame 0.
- **Captions:** "metres".
- Rerun every gate (open gate, sfx level, music_gate on the same bed, polish, picture_qa) on v02.

J2248 stays parked until v02 has these changes in it. Don't schedule anything. Mon 9 Nov 11:30 is still taken
by `iyvWYFP_ETA`, and the 21 Nov date is provisional.
