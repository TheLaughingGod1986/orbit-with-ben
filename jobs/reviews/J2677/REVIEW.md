# J2677: what the weekly OWB audit (J2366) did not measure

By Claude Code on the MacBook (agent `macbook`), 12 Nov 2026. Read-only, £0. No Studio, YouTube, schedule or cut change, and nothing here authorises one.

## Verdict: FIX (four of the eight parts measured, four not)

| Part | Result |
|---|---|
| Shorts retention curves, biggest-drop second | **Not measured.** The 12 Nov snapshot carries curves for longs only, and this MacBook has no `07_Content-Ops/.env`, so no Analytics call can be made here. |
| Search terms | **Not measured.** Same reason. |
| Frame 0 | Measured from the cut metas and the 9 Nov first-second audit. |
| First cut | Measured (same sources). |
| Payoff time | Measured where the meta records it (six of ten Shorts). |
| Loop | Measured from the metas (method, loop sentence, silent tail). |
| SEA | **Not read.** No `yt-dlp` on this MacBook, and web fetch and `curl` are not allowed in the unattended run. |

The three unmeasured parts need the Mini (Analytics sign-in, `yt-dlp`). A follow-up job is queued for it; see the end.

## Sources

- Views, stayed-to-watch and average viewed: J2366's table (`05_Analytics/weekly_audit/OWB_2026-11-12.md`, Studio lifetime read 11 Nov). Not re-read.
- Edit facts: each aired cut's own `_meta.json` (the file named in `UPLOADS.json`), and `00_Brand/Channel-Setup/audits/SHORTS_FIRST_SECOND_AUDIT_2026-11-09.md` (J2429).
- No media file was opened. Every edit figure is what the build recorded, not a new measurement of the picture.

## The ten Shorts

| Short | Length | Stayed | Avg viewed | Frame 0 | First cut | Payoff | Loop |
|---|---|---|---|---|---|---|---|
| `T9fVlG3CCzU` Shooting Stars | 20.0 s | 49.8% | 66.4% | Full-frame still (ISS Perseid streak), slow zoom 1.00 to 1.06 | 4.7 s | "between a grain of sand and a pea", overlay 6.5–8.9 s | Crossfade back to the opening plate; last word 17.0 s, then 3.0 s with no voice; last line does not run into line 1 |
| `VfDm3E2bUgU` 16 Sunrises | 18.9 s | 31.6% | 66.7% | not read | not read | The title's number is in line 1; "16 sunrises, 16 sunsets" overlay 14.05–17.45 s | Last word 17.76 s; method not read |
| `hZH0C7fpCk4` Venus 95% | 19.7 s | 31.6% | 66.2% | not read | 2.25 s | "second Earth" at 14.58 s (74% in) | Forward; "…closer to the sun. Venus is ninety-five percent as wide as Earth." |
| `_a66uhRDips` Venus melt lead | 17.4 s | 32.8% | 91.7% | not read | 2.29 s | "two hours" at 15.49 s (89% in) | Forward; "…much more than two hours. Venus is hot enough to melt lead." |
| `1OCNzhkiBuc` Neptune winds | 20.6 s | 42.6% | 75.0% | Full-frame moving Voyager 2 clouds | 2.70 s | "over two thousand kilometers an hour" in sentence 2 (sentence 1 ends 1.62 s; exact time not recorded) | Forward; last word 19.45 s; "And still. The wind on Neptune is supersonic."; loop check PASS |
| `ZpEA8stoSPA` Uranus winters | 21.2 s | 26.9% | 306.8% | Still in "fit" mode (picture padded, not full frame), zoom 1.25 to 1.42 | 5.9 s | "Uranus is tipped 97 degrees", overlay 6.4–9.0 s | Crossfade back to the opening plate; last word 18.16 s, then 3.0 s with no voice |
| `gJwNJN_yMKU` Apophis | 18.8 s | 34.5% | 231.0% | not read | 2.4 s | 13.57 s (72% in) | Forward; "…and watch. Apophis will fly closer than some of our satellites." |
| `6dcL5rBmHPM` Saturn's rings | 22.8 s | 21.7% (45 views, too few) | 66.7% | not read | 2.6 s | "ten metres" at 18.74 s (82% in); also said in line 1 | Forward; "…open space again. Saturn's rings are only about ten metres thick." |
| `iyvWYFP_ETA` Mars night (44 h read) | not read | 38.8% | 62.6% | Pushed still (J2429: frame-0 movement 0.14 against a 1.50 floor) | 4.10 s | not read | not read |
| `ffYKoNVPoqg` Titan v11 (20 h read) | 18.0 s | 39.6% | 48.8% | First-second gate PASS (J2429) | 2.67 s | Line 1: "15 meters underwater" | Forward; last word 16.13 s |

## What the numbers do and do not show

- **A fast first cut alone has not lifted stayed-to-watch.** Six Shorts cut at 2.25–2.70 s; they stayed 21.7% to 42.6%. The best stayed figure (Shooting Stars, 49.8%) held its first shot 4.7 s. The worst mature one above 100 views (Uranus, 26.9%) held 5.9 s on a padded still. So a long hold on a padded still fits the worst result, but a short first shot is not enough.
- **The two Shorts that open on something other than a full-frame picture of the subject moving are at the bottom or middle.** Neptune is the only one of the ten recorded as moving footage at frame 0, and it has the second-best stayed figure (42.6%). One Short is not a finding.
- **A late payoff has not hurt average viewed.** Venus melt lead pays off at 89% of its length and has 91.7% average viewed. The Shorts paying off at 72–82% read 66.2%, 66.7% and 231.0%.
- **Loop method does not explain the two rewatched Shorts.** Uranus (306.8%) uses a crossfade with 3 s of no voice; Apophis (231.0%) uses a forward loop with a sentence that runs on. Shooting Stars has the same crossfade ending as Uranus and reads 66.4%.
- Eight mature Shorts, one of them under 100 views. None of this is strong enough for a rule.

## One next-video change each (Chief decides)

1. **Retention curve and biggest-drop second:** none proposed. Without the curve, where viewers leave is still unknown; the follow-up job pulls it.
2. **Search terms:** none proposed, for the same reason.
3. **Frame 0:** the next Short built opens on full-frame moving footage of the titled subject, not a zoomed still. This is already LEARNINGS rule 24; the evidence here (Neptune 42.6% moving, Uranus 26.9% padded still) agrees with it and adds nothing new.
4. **First cut:** J2429 recorded `HZGTovJu_TQ` (026, scheduled Mon 16 Nov) holding its first shot 4.8 s. It is the next Short to air with that fault. A re-cut of a scheduled Short is the Chief's call and needs Ben's watch; I did not open the cut.
5. **Payoff time:** record `first_cut_s` and `payoff_number_s` in every standalone Short's meta, as the lifted Shorts already do. Four of the ten had no recorded payoff time, so the comparison above is incomplete. No edit change is supported by these numbers.
6. **Loop:** run one test, not a rule: on the next standalone Short, end on a line that runs into line 1 with a forward loop and under 1.5 s without voice, and compare its average viewed with the crossfade endings (Shooting Stars 66.4%, Uranus 306.8%).
7. **SEA:** none; not read.

## Not checked

- No media opened, no frame looked at, nothing listened to.
- The J2366 Studio figures were copied, not re-read.
- Frame 0 for five Shorts and the loop method for two were not in the fields I read in the time.
