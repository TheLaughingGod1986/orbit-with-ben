# J0068 progress — Cursor covering, 9 Oct 2026 01:28–01:50 BST

No v03d render yet. This run did the music bed and the picture homework for the next run.

## Music bed (item 2)

- Credits before: 56,821 left (of 209,536). The 022 bed (525 s) cost 7,219 on 7 Oct, so a 500 s bed was estimated at ~6,900 and would have left ~49,900, above the 30,000 floor.
- Generated once: `05_Music/mars-robot_score_bed_v01.mp3` (song id `iv4C0yzn1F3GEs8CbLnm`), with the exact prompt from the job, `--length-ms 500000`.
- **The API returned 182.99 s, not 500 s.** It is −16.7 LUFS integrated. 021's bed is 540.0 s and 022's is 525.0 s, so earlier calls returned the full length.
- Cost: the usage API shows Music 2,515 credits on 9 Oct. The subscription counter still read 56,821 at 01:40 (it lags). Logged in `04_Audio/elevenlabs_ledger.jsonl` and `scripts/ai_spend.py`.
- The VO runs to 486.7 s, so the bed covers about 37% of the cut. **The job allows one generation only, so this needs Claude's call:** loop the 183 s bed with crossfades to the full runtime, or allow one more take (about 4,300 credits for the missing ~310 s; ~45,000 would still be left).
- Not listened to by ear yet.

## 2:54 swap (item 1)

- PIA12102 (`nasa_pool_v01/spirit/PIA12102.jpg`) is 4396×2061, so filling 16:9 needs a 0.52× downscale. **Use it**; PIA12205 (731×597, 2.63×) is not needed.
- PIA12102 is not used anywhere in v03c. PIA12337 is used once (cut 39, row 14, 170.73–175.97 s).

## Opening (item 6a)

v03c row 1 (0–5.67 s) is PIA24765. The first sentence is "A robot built to last ninety days on Mars kept going for more than fourteen years." These real Opportunity pictures show the rover itself:

| id | what | size | uses in v03c |
|---|---|---|---|
| PIA15115 | Dusty Mars Rover Self Portrait (deck + panels) | 4796×3993 | 1 (row 4) |
| PIA20328 | Opportunity Shadow and Tracks on Martian Slope | 1290×1285 | 1 (row 13) |
| PIA07372 | Opportunity Self-Portrait, Sols 322-323 | 8000×7253 | 2 (rows 2, 22): at the cap |
| PIA16120 | Shadow Self-Portrait at Endeavour Crater | 620×582 | 0, but 3.1× too small |
| PIA17956 | Shadow Portrait of Opportunity on Martian Slope | not in pool | NASA API hit; would need harvesting |

PIA15115 is the strongest choice for frame 0: the rover is the subject, it's large, and it's used only once.

## Panel cleaning (item 6e)

- The NASA pair exists and is already in the pool: **PIA17759** (Pancam self-portrait, Jan 2014, dusty) and **PIA18079** (Pancam self-portrait, late Mar 2014, "freshly cleaned"). Same rover and same camera. PIA18080 is the false-colour version of the cleaned one.
- **v03c shows them in the wrong order.** It has PIA18079 (clean) at 264.13–269.67 s and then PIA17759 (dusty) at 269.67–274.57 s. But "swept its panels clean" is spoken at 261.6–262.6 s, and "cleaning events" at 264.7–265.1 s.
- Each image is already used twice in v03c (PIA17759: rows 5 and 20; PIA18079: rows 20 and 21). So the matched before→after in rows 20–21 must replace those uses, not add to them.
- NASA API searches that returned nothing: "Opportunity solar panels before after cleaning", "Spirit solar panels cleaning event", "Opportunity rover deck dust".

## Not started

Items 6b (name labels), 6c (one machine per passage), 6d (wheel-holes hold), the v03d assembler, the render, picture_qa, music_gate and the similarity matrix, and the phone copy.
