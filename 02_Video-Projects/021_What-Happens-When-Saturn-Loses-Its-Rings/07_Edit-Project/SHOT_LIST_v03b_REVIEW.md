# Saturn shot list v03b: row review (1 Oct 2026)

v03b passes `check_shot_list.py`, and I read all 107 rows against their VO lines. Most rows fit. The fixes below are what the checker can't catch: a picture that contradicts its words, or a script lock that was missed.

**`shot_list_v03c.csv` = v03b with the picture swaps in section A applied.** It passes the checker, with the same timings and no reuse. Sections B and C still need Ben's decision before assembly.

## A. Picture swaps (applied in v03c)

| Row | VO | v03b | v03c | Why |
|---:|---|---|---|---|
| 30 | "or in boulders the size of a house" | PIA01486 (Voyager composition map) | **PIA10081** (ice-chunk illustration) | It is the one picture that shows chunks. Its "Illustration" caption moves with it. |
| 77 | "a heavy, ancient ring would still be heavy" | PIA10081 | **PIA01486** | Straight swap with row 30. |
| 47 | "guided down, along the magnetic path, into the upper atmosphere" | PIA08990 (D ring) | **PIA13402**, caption "Saturn's magnetic field" | The D ring is Cassini's equatorial leak. The script keeps it apart from the magnetic rain. |
| 48 | "Water, arriving from above. Ring rain." | PIA17150 (D ring) | **PIA21337** (polar cap, atmosphere) | Same reason. No aurora under a "rain" line. |
| 49 | "We did not need a spacecraft inside that rain" | PIA18321 (D ring) | **PIA18290** (cloud bands) | Same reason. |
| 50 | "Astronomers on Earth, using the Keck telescope…" | PIA21892 (Cassini, 13 Sept 2017) | **PIA03162** (Hubble, distant full disk) | A Cassini close-up contradicts "we did not need a spacecraft". A distant telescope view matches. No caption. |
| 51 | "and measured how fast the ice was leaving" | PIA21345 | **PIA03160** (Hubble) | Same reason. |
| 58 | "the D ring — straight into Saturn's equator" | PIA21895 | **PIA17150** (Dusty D Ring by the limb) | The D-ring pictures belong here. |
| 59 | "That equatorial inflow is a heavier leak…" | PIA21356 | **PIA08990** (D-ring structure) | Same reason. |
| 61 | "So how long does the bright sheet have?" | PIA21343 | **PIA21345** ("So Far from Home") | Cassini's last distant look at the rings under the question. |
| 89 | "Saturn is still there. Pale gold bands." | PIA18294 (rings in shot) | **PIA21888** (bands only) | This section is Saturn *without* rings. |
| 94 | "It was the ice in orbit around the body" | PIA21888 | **PIA18294** | Straight swap with row 89. Here the rings are wanted. |

These pictures are now spare: PIA21892, PIA21895, PIA21356, PIA21343, PIA18321.

## B. Script locks missed (Ben to decide)

1. **Orbit's first beat is in the wrong place.**
   - **The script says:** Orbit appears after the open, "small beside the ring plane, looking along the ice", at the line now read as "Does the fall ever stop?" (row 21).
   - **v03b instead:**
     - It has no Orbit there.
     - It puts `orbit_tumble_omni.mp4` at row 36, "Drop through those ten metres", where the script says **No Orbit**.
     - It runs that clip from 0 to 5.5 s, but only 0–3 s of the tumble was approved.
   - **Proposed:** Orbit goes to row 21, using an approved Omni clip of at least 3.5 s of usable footage. Row 36 becomes NASA **PIA09908** ("Northward Through the Rings", spare).
   - **Blocker:** if the only Orbit clip is the 3 s tumble, that needs the Vertex Omni retry first.
2. **Three of the five chapter cards are missing.** The script locks five cards of about 1.5 s each. v03b has only "The Rain Into Saturn" and "Saturn Without Them". Missing:
   - "The Rings Are Falling" (after row 5);
   - "Ice, Not Rock" (before row 26);
   - "When the Rings Were New" (before row 70).

   If they were dropped on purpose when the VO was tightened, record that here. Otherwise insert them. That means splitting the VO at those paragraph breaks and adding about 4.5 s in total; the audio itself is unchanged.
3. **Confirm the Omni clips exist and are approved:** `orbit_tumble_omni.mp4` and `orbit_bare_omni.mp4`. Omni on Vertex was still failing at the last report.

## C. Goddard clip (row 44)

SVS 12672, "Saturn's Rings Are Disappearing", is the right video. Its page asks for the credit "NASA's Goddard Space Flight Center". The checker now adds that line to the credits file automatically.

The video carries narration and licensed music (Killer Tracks), so:
- use the **picture only, muted**;
- check that the 5.6 s used has no on-screen text.

## Optional (not applied)

- Row 82, "What if a moon came too close, and came apart?", sits over PIA06425, a ring temperature map. PIA18277 ("Clumpy Ringlets", spare) reads more like rubble.
