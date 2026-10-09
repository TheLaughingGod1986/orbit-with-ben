# Shorts tests A and B (Ben said yes, 9 Oct 2026)

Ben, 9 Oct: *"A and B yes let's get and test results."* Claude owns both tests and reads them out on the board and on #99.

## A. One Short per film is the long's own opening (Orbit With Ben)

**Change.** For each long from 025, one of its three Shorts is the long's own opening: the first 30–38 s of the master, reframed to 9:16, with the long's own voice and music, cut on a sentence end before 40 s. It still has to pass `gate_shorts_open` (frame 0 shows the titled subject, no Orbit at frame 0, and no opening background reused from the last 10 Shorts). Its Related video is the long. It replaces one of the three planned Shorts, so the film stays at three Shorts and one a day. The replaced script is kept for a later slot.

**Day rotation,** so the weekday doesn't decide the result:

| Film | Opening Short replaces | Day |
|---|---|---|
| 025 Mars | Wed 11 Nov ("minus 90", which also shares its hook with thumbnail C) | Wed |
| 026 Nearest Star | Fri 20 Nov | Fri |
| 027 Earth Spin | Mon (its first Short) | Mon |
| 028 | Wed | Wed |

It starts with 025, after the Familiar Danger four-week test (12 Oct – 6 Nov) ends, so the two tests don't mix.

**What we compare.** Each opening Short is compared against the same film's other two Shorts (same topic, same week):
1. Day-1 Shorts-feed share (the house measure: 50% or more means fed).
2. Views at 7 and 28 days.
3. Average % viewed.
4. **Views of the long that came from Shorts.** These are the long's YouTube Analytics traffic source `SHORTS`, credited to the week that Short ran.

**Pass:** across the four films, the opening Shorts match or beat the others on day-1 feed share and views, and the long gets more views from Shorts in its opening-Short week. If that holds, the opening Short becomes standard. If not, we stop.

**Readouts:**
- First: Wed 18 Nov (025, 7 days).
- Then: Wed 9 Dec (025, 28 days, plus 026 at 7 days).
- Final: early January (028 at 28 days).

## B. History of Science: fewer feed Shorts, more search-titled ones

**Change, from HOS 007 (airs 12 Nov):**
- **Two Shorts per film, not three.** This also saves about a third of the Shorts voice credits.
- **Each Short is titled as the question people type.** For example "Why are vaccines named after a cow?", not a feed-style teaser. Check the title against signed-out YouTube autocomplete (`public_search.py`) before it's locked.
- **The Short's first line answers the start of that question.**
- **Long titles get the same autocomplete check before lock.**
- 005 and 006 stay as planned (already voiced).

**Baseline:** the 13 HOS Shorts already aired plus 005 and 006 (the J0087 table: views, feed share, search share, title vs subject).

**What we compare,** for search-titled Shorts against the baseline:
1. Share of views from YouTube search.
2. Views at 28 days.
3. Average % viewed.

For the HOS longs: search share and impressions at 28 days.

**Pass:** the search-titled Shorts get a clearly bigger search share (at least double the baseline), with 28-day views no lower per Short. That means two Shorts per film do at least the work of three.

**Readouts:**
- First: about 10 Dec (007's Shorts at 28 days).
- Final: early January (010).

## Where the numbers come from

The channel tracker's daily snapshot (`05_Analytics/owb|hos/snapshots/`, traffic sources per video). Claude posts each readout as a table on #99 and puts the headline on the board.
