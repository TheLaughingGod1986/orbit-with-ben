# 025 v03d: one machine per passage (J0068 item 6c)

Cursor covering, 9 Oct 2026 03:15 BST. I checked every cut in `cuts_v03d.json` against the words spoken over it (`mars_robot_words_list.json`) and the pool titles. Generic passages (Mars conditions, dust in general, the summing-up rows 28–31) are not counted.

## Cuts where the picture is a different machine from the one being narrated

| film time | row | now | narration | same-machine candidate in the pool (uses in v03d) |
|---|---|---|---|---|
| 3:14 (194.3–198.7) | 15 | PIA16933 *View Back at Record-Setting Drive by **Opportunity*** | Spirit: "ninety days. It worked for more than six years." | PIA12142 *Spirit View from Troy* (1). PIA12205 is 2.63×, which is over the cap. |
| 4:14 (254.5–258.9) | 20 | PIA07458 *Dust Devils Seen by **Spirit*** | "Opportunity should have starved within months…" | PIA22909 *Opportunity Legacy Pan (True Color)* (0), or PIA07108 *Frost on Mars Rover Opportunity* (0). |
| 4:43 and 4:53 (283.3–289.3, 293.7–298.7) | 21 | PIA22520 *Curiosity's View of the June 2018 Dust Storm* (×2; Claude reviewed_ok, #6066558180) | Opportunity's last signal and the eight months of commands | PIA22549 *Opportunity After the Dust Storm* (0), PIA23092 *Goodbye Opportunity* (0), PIA22929 *Opportunity's Last Message* (0). These need a full-size look first, because the last two may be a graphic or plot (picture_qa FAIL). |
| 5:31 and 5:36 (331.0–340.7) | 24 | PIA23305 *Power for Mars 2020* and PIA23306 *Mars 2020's MMRTG* (Perseverance's unit) | "Curiosity runs on a nuclear power source…" | **None.** The pool has no picture of Curiosity's own power source. I left these, since the two rovers use the same type of unit. |
| 6:36 (396.0–401.1) | 27 | PIA18093 *Endeavour Crater Rim From Murray Ridge* (Opportunity's view) | Ingenuity: "test flights over 30 days in air 1% as thick as ours." | PIA25686 *Perseverance's Mastcam-Z Views Ingenuity's 47th Takeoff* (0), PIA24644 *Ingenuity's Shadow During Third Flight* (0), or PIA24542 *Perseverance's Selfie with Ingenuity* (1). |

## Passages that are already all one machine

- Opportunity open, rows 1–2.
- Spirit at Troy, row 14.
- Phoenix, row 16.
- Opportunity cleaning, row 20 from 258.9.
- InSight, row 23.
- Curiosity wheels, row 25.
- Ingenuity, row 27 apart from 396.0.

## Not swapped in v03d

The v03d render was already finished and gated when this audit was done. Any swap means a re-render plus picture_qa again, so it would be a v03e. Upscale and fill for each candidate are to be checked with the assembler's `--plan` before rendering.
