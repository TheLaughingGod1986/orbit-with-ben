# Competitor thumbnail and title study — 28 October 2026

J1106 worker evidence, not Chief approval. Five named channels collected; search-neighbour extension is now complete in [the companion study](2026-10-28_COMPETITORS_EXTRA.md). No thumbnails, titles, tests or YouTube state changed.

## Method and limits

Captured 2026-10-28T17:31:51.036960+00:00; window begins 2026-07-30T17:31:51.036960+00:00. Public YouTube channel tabs and yt-dlp watch-page metadata only. Videos and Shorts use their actual channel tabs, not a duration guess. Exact upload timestamps/dates replace approximate tab dates before filtering. Views per day = lifetime views / age in days; the collector has a one-day floor, but **no selected upload was younger than one day**, so that floor changes no rank. Public counts are a discovery proxy, not impressions, CTR or proof of thumbnail causation.

The latest 200 entries were listed per tab. Every capped primary tab reaches uploads older than this 90-day window; uncapped tabs are exhausted. Five members-only SEA uploads are explicitly excluded. HOTU exposes no Shorts tab; melodysheep has no long in the window (latest long dated 16 June 2026). Thumbnail/title variants may change between listing and watch reads; the captured watch title is the ranked evidence, not a claim about the title throughout the video’s life.

An initial player-format request produced sign-in/bot errors. Repeating as metadata-only with `--ignore-no-formats-error` recovered the public metadata without cookies or sign-in. Remaining exclusions are membership-only. Raw outputs stay in `_desk/j1106/competitors/details`; do not commit them, since full yt-dlp JSON can contain temporary media URLs.

**No cohort contains 20 uploads.** Fastest ten and slowest ten therefore overlap; they are not independent winner/loser samples. Where fewer than ten exist, all are shown. Do not pad with old videos, infer zero uploads from a request failure, or attribute view velocity to packaging alone. Large channels, topics, video ages and promotion differ.

## Cohort coverage

| Channel | Format | Public uploads in 90d | Fast/slow overlap |
|---|---|---:|---:|
| astrum | videos | 15 | 5 |
| astrum | shorts | 4 | 4 |
| hotu | videos | 1 | 1 |
| hotu | shorts | 0 | 0 |
| sea | videos | 2 | 2 |
| sea | shorts | 1 | 1 |
| kurzgesagt | videos | 7 | 7 |
| kurzgesagt | shorts | 13 | 7 |
| melodysheep | videos | 0 | 0 |
| melodysheep | shorts | 1 | 1 |

## Ranked public inventory

All 44 selected thumbnails are saved and visually coded in `competitor_visual_coding.csv`: visible words, relative text size/colour, object/face/scene, composition, curiosity gap, title shape/length/hook, and numeric contrast/darkness. Small illegible text is explicitly marked. Image statistics measure the entire fetched rendition, including Shorts side panels; they are descriptive, not OWB crop gates. Sheets are `_desk/j1106/competitors/sheet_1.jpg` through `sheet_4.jpg`.

| Channel / format | Video and captured title | Published | Views/day | Fast 10 | Slow 10 |
|---|---|---|---:|---|---|
| astrum / videos | [Uranus: The Weirdest Planet In The Solar System](https://www.youtube.com/watch?v=pZh5BWCNmmE) | 2026-10-27 | 258,019 | yes | no |
| astrum / videos | [Have We Finally Found a New Theory of Everything?](https://www.youtube.com/watch?v=c8dfuXDGbB4) | 2026-10-14 | 82,171 | yes | no |
| astrum / videos | [What Is Hiding In The Milky Way's Core?](https://www.youtube.com/watch?v=T9HLYPn59S4) | 2026-10-21 | 69,702 | yes | no |
| astrum / videos | [What Is It Like on the Surface of a Black Hole Planet?](https://www.youtube.com/watch?v=PxJSOWyYWkc) | 2026-10-01 | 51,917 | yes | no |
| astrum / videos | [The Surprising Danger of Building a Human Colony on the Moon](https://www.youtube.com/watch?v=UPWQimElMhQ) | 2026-09-16 | 49,513 | yes | no |
| astrum / videos | [Why Is the Closest Planet to the Sun So Cold?](https://www.youtube.com/watch?v=YQ7DWNhjOpk) | 2026-09-02 | 45,882 | yes | yes |
| astrum / videos | [Could Neptune’s Moon Triton Be Habitable?](https://www.youtube.com/watch?v=MGQcrX7DMYw) | 2026-10-07 | 39,385 | yes | yes |
| astrum / videos | [We Found Something Unexpected at the Heart of the Milky Way](https://www.youtube.com/watch?v=B3c6IFY94Cw) | 2026-09-29 | 34,166 | yes | yes |
| astrum / videos | [We Just Saw the Birth of One of the Strangest Objects in the Universe](https://www.youtube.com/watch?v=tlmj5ThgWbY) | 2026-09-23 | 24,657 | yes | yes |
| astrum / videos | [You Can’t Land on Saturn's Moon Hyperion](https://www.youtube.com/watch?v=4ZnN44BTTjU) | 2026-08-13 | 22,970 | yes | yes |
| astrum / videos | [Have We Finally Found a Real Wormhole?](https://www.youtube.com/watch?v=1_8cel49X30) | 2026-08-05 | 20,740 | no | yes |
| astrum / videos | [We Caught a Black Hole Switching On For the First Time](https://www.youtube.com/watch?v=jbwrsQ9kG_o) | 2026-08-27 | 18,566 | no | yes |
| astrum / videos | [Earth’s Entire Existence In One Video](https://www.youtube.com/watch?v=S3emb6rHDZ0) | 2026-08-24 | 14,698 | no | yes |
| astrum / videos | [NASA Found Huge Structures Hidden Inside Mars](https://www.youtube.com/watch?v=SPoDl0Cnc0o) | 2026-08-19 | 12,810 | no | yes |
| astrum / videos | [We Measured Dark Energy in Our Solar System for the First Time](https://www.youtube.com/watch?v=fPIiJ3iZoJ4) | 2026-09-09 | 11,923 | no | yes |
| astrum / shorts | [The Most Detailed Image Ever Taken of the Sun](https://www.youtube.com/watch?v=fsYQ3cubV6o) | 2026-09-28 | 115,943 | yes | yes |
| astrum / shorts | [The Andromeda Galaxy Is Under Attack](https://www.youtube.com/watch?v=Is7z49LToNg) | 2026-08-28 | 30,052 | yes | yes |
| astrum / shorts | [Planet Formation Explained in Two Minutes](https://www.youtube.com/watch?v=08n0VB4V5SA) | 2026-10-09 | 1,873 | yes | yes |
| astrum / shorts | [General Relativity Explained in Two Minutes](https://www.youtube.com/watch?v=NJnneBgxWJg) | 2026-09-17 | 1,526 | yes | yes |
| hotu / videos | [Is The Entire Universe Quantumly Entangled?](https://www.youtube.com/watch?v=cqGhCCDC_Sw) | 2026-10-08 | 25,731 | yes | yes |
| sea / videos | [The Real Largest Star](https://www.youtube.com/watch?v=-nIsOi-tVKM) | 2026-10-25 | 70,485 | yes | yes |
| sea / videos | [Higgs Boson: The God Particle](https://www.youtube.com/watch?v=7oR0Pmd-WIk) | 2026-08-23 | 7,972 | yes | yes |
| sea / shorts | [The Cold Spot: The Biggest Mystery in Cosmology #space #universe #mystery](https://www.youtube.com/watch?v=_5J1V-INKoc) | 2026-08-13 | 186 | yes | yes |
| kurzgesagt / videos | [How I Survived Late-Stage Cancer (A Fun Story)](https://www.youtube.com/watch?v=5_Fayfx2NUM) | 2026-10-27 | 3,310,211 | yes | yes |
| kurzgesagt / videos | [AI Just Crossed the Terrifying Line - Now What?](https://www.youtube.com/watch?v=ujkD4SxPKOI) | 2026-10-05 | 988,339 | yes | yes |
| kurzgesagt / videos | [You Will Only Like Half of This Video](https://www.youtube.com/watch?v=PXbVn-f_wuM) | 2026-10-20 | 655,987 | yes | yes |
| kurzgesagt / videos | [We Finally Know More About Humanity’s First Civilization](https://www.youtube.com/watch?v=_y9JuojAIg0) | 2026-10-08 | 557,383 | yes | yes |
| kurzgesagt / videos | [This Woman Cured Her Cancer with an Insane Method](https://www.youtube.com/watch?v=0NY2gAftzJE) | 2026-09-15 | 493,989 | yes | yes |
| kurzgesagt / videos | [This Is What a Godlike Civilization Would Look Like](https://www.youtube.com/watch?v=QW_jlUn4gA8) | 2026-09-22 | 256,478 | yes | yes |
| kurzgesagt / videos | [Why Humanity Will Never Leave The Solar System](https://www.youtube.com/watch?v=Cyl3X88KEgg) | 2026-08-04 | 125,505 | yes | yes |
| kurzgesagt / shorts | [What If We Cool Down the Sun?](https://www.youtube.com/watch?v=35No369rmq0) | 2026-10-24 | 204,337 | yes | no |
| kurzgesagt / shorts | [Can Earth Run Out of Water?](https://www.youtube.com/watch?v=tZ8i1RxGSYM) | 2026-08-31 | 69,168 | yes | no |
| kurzgesagt / shorts | [What If You Never Slept?](https://www.youtube.com/watch?v=hiIIGMeMEuE) | 2026-09-03 | 52,623 | yes | no |
| kurzgesagt / shorts | [Dust Is Not What You Think](https://www.youtube.com/watch?v=YqAI0oqtt7w) | 2026-08-27 | 47,558 | yes | yes |
| kurzgesagt / shorts | [Humans Can Regrow an Organ](https://www.youtube.com/watch?v=oNTaHYXQ4MM) | 2026-09-26 | 46,338 | yes | yes |
| kurzgesagt / shorts | [Your Brain on Magic Mushrooms](https://www.youtube.com/watch?v=b1EMX3wyqCY) | 2026-09-28 | 41,292 | yes | yes |
| kurzgesagt / shorts | [How Stress Changes Your Brain](https://www.youtube.com/watch?v=IvtsVHzMLwY) | 2026-08-22 | 29,799 | yes | yes |
| kurzgesagt / shorts | [What If Gravity Was 10% Stronger?](https://www.youtube.com/watch?v=EqkRVbaBxtg) | 2026-08-29 | 24,215 | yes | yes |
| kurzgesagt / shorts | [How Antidepressants Work](https://www.youtube.com/watch?v=w5RZfxQHxyY) | 2026-08-20 | 19,153 | yes | yes |
| kurzgesagt / shorts | [How ADHD Medication Works](https://www.youtube.com/watch?v=NIifnIP_NnQ) | 2026-09-05 | 18,177 | yes | yes |
| kurzgesagt / shorts | [Your Skeleton Is Electric](https://www.youtube.com/watch?v=RQprZZJIb6Y) | 2026-09-24 | 15,291 | no | yes |
| kurzgesagt / shorts | [Why Ebola Keeps Coming Back](https://www.youtube.com/watch?v=OKsWuqNjomQ) | 2026-08-24 | 14,690 | no | yes |
| kurzgesagt / shorts | [What the Flu Does to Your Body](https://www.youtube.com/watch?v=U5-dE2nCzjM) | 2026-08-17 | 10,218 | no | yes |
| melodysheep / shorts | [Let's hope this never happens.](https://www.youtube.com/watch?v=9kReABqC9c4) | 2026-10-15 | 8,907 | yes | yes |

## Observations to test, not adopted rules

1. **A clear environment can make a subject feel immediate.** Astrum’s Uranus view, black-hole-planet horizon and Moon-base scene are among its first five by velocity. Several of its last five use a small luminous blob or isolated object. But the slow Mars cover also names its subject clearly. Naming alone does not separate the groups. Test a clear whole subject plus one scale reference; retain OWB’s yellow hook and text band.
2. **Scale is legible without a sentence.** SEA’s largest-star cover places a tiny Solar System marker against a huge stellar limb. Its other eligible long is the Higgs film with no words; with only two videos there is no reliable fast/slow pattern. Use the scale relationship as a composition hypothesis for Last Star/Andromeda, not evidence to abandon OWB text rules.
3. **Borrow visual hierarchy, not threat language.** Kurzgesagt’s most-viewed-per-day covers have simple dominant shapes, large white labels and saturated colour. The same treatment appears lower down its list. “95% DEATH RATE” and “WE LOST CONTROL” are not OWB’s voice. The sampled Astrum Shorts range from a clear solar close-up to compact explainer labels, but only four exist; Shorts thumbnails do not establish their moving first frames.

## Search extension and remaining work

Three provisional OWB candidate titles were searched through nonpersonalized public yt-dlp search. Last Star ranked second, behind Kurzgesagt; the compilation ranked first; Andromeda was absent from the first ten. These are timestamped snapshots, not universal rankings. `competitor_search.json` preserves all returned rows.

Andromeda’s result set adds What If, PBS Space Time, The Secrets of the Universe, NASA Video, Science Time, VideoFromSpace, Calm Space, Dr. Becky and Khan Academy. The last is a broad educational channel included because it outranked this space title; Chief may keep it as a topic neighbour rather than a channel-wide comparator. Both tabs were catalogued where exposed. Exact 90-day ranking and thumbnail downloads are running in `j1106-extra-study`; no extra-channel design pattern has been inferred yet.

Next: read the detached completion marker and errors; review its chronological stopping boundaries and any 1,000-entry cap; code the extension’s selected thumbnails; complete the remaining Short crop/frame checks; then build the three Bs and title alternatives, run independent panels and hand off to Chief. Do not arm a title and thumbnail test simultaneously or replace an existing test. No new test exists yet.

## Extension completion update

The detached collection exited 0; all 206 selected extra-channel thumbnails have now been inspected and coded, with ranked tables and limits in [the extension](2026-10-28_COMPETITORS_EXTRA.md). The earlier running-task paragraphs above describe the prior checkpoint, not current process state. No detached collector remains active.
