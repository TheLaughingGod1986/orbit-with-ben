# Field Order History: launch playbook

Claude's plan, 17 Nov 2026, for Ben's goals: monetised as fast as possible, then a lot of views. The rules are in
`studio/RULES.md`; this is how we play.

1. **The deadline that matters.** From 1 Feb 2027 YouTube asks new channels for 8,000 watch hours, double today's 4,000
   (YouTube blog, 10 Aug 2026). Applying before then needs 1,000 subscribers and 4,000 public watch hours first, and
   review takes about a month. So December is a sprint: as soon as Ben's voice plan allows, make three films a week
   through December. The day the channel has 1,000 subscribers and 4,000 hours, apply.
2. **Launch burst.** Go live with the first films close together (pilots 1 and 2 in the first week, pilot 3 as soon as
   it can be voiced), then two a week. Every fast-growing channel we studied sat near zero for 5-20 videos until one
   film took off; more films early means more chances at that film.
3. **Packaging lab.** For every film, write at least three titles and two thumbnail ideas before the script, score the
   titles (Claude's vidIQ title score on request) and pick the best. After upload, run Test & Compare on the
   thumbnail. Pilot picks, scored 17 Nov: "How Britain Built Two Harbours in Secret and Floated Them to Normandy" (91,
   against 88 for the plan's title); "How the Allies Closed the U-Boats' Safest Hunting Ground" (91, against 86; the
   "600-mile" figure could not be confirmed); "Why America's Most Expensive WW2 Weapon Wasn't the Atomic Bomb" (99, against 91).
   Evidence (vidIQ outlier study, 17 Nov: 260 long WW2/military videos from the last 12 months, 184 on channels under
   50k; multiple = views against the channel's usual): a superlative 14.5x against 6.8x without (22 videos); the other
   side's recorded reaction 11.0x (49); an "until/then" turn 10.2x (18); a hard number that is not a year 8.6x (70);
   How/Why openers neutral; series names 5.5x and What/When openers 5.6x; titles of 50 characters or fewer 17.0x (11)
   against 7.1x for 51-70 (61). Thumbnails, top 20 against bottom 20: real black-and-white archive photo 10 to 4, no
   text 8 to 4, dark grade 2 to 10. Correlation from an outlier feed, not proof; re-test on our own films.
4. **Series and binge.** Every film belongs to a series with its own playlist: *Engineering that won the war*, *The
   supply war*, *Deception*. End screen: the next film in the series, plus subscribe. Pinned comment: the sources and
   one question for viewers. A viewer's second film is the cheapest watch time there is.
5. **Watch-hour multiplier.** After 8 films, publish one 2-3 hour compilation of a series, made of our own films with a
   new opening and chapter links. At most one compilation per 8 new films, so new films always stay the large majority.
6. **The 48-hour read.** For each film, record impressions, click-through rate, average view duration and views at 48
   hours and at 7 days in `05_Analytics/READS.md`. With over 1,000 impressions and click-through under 3% at 48 hours,
   change the thumbnail first, then the title. With average view duration under 25%, the next script tightens its
   first two minutes.
7. **Topic engine.** Keep ten checked topics ready at all times. After six films, choose the next topics two to one
   from the type of film that is doing best. Refresh the niche packaging library (`05_Analytics/PACKAGING_LIBRARY.json`
   and `05_Analytics/PACKAGING_FINDINGS.md`) monthly via a read-only YouTube Data API pull across the tracked WW2
   channels so title and thumbnail choices stay grounded in current outlier evidence.
8. **Upload time.** 17:00 London (12:00 New York), to catch the UK evening and the US midday. Move it once the channel's
   own "when your viewers are on YouTube" chart says otherwise.
9. **Who runs it.** The Chief owns this channel's queue; it is not a side project. The next job on the critical path
   (script, then voice, then edit, for the next film due) is always marked urgent, one job at a time.
