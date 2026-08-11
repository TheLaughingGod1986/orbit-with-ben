# Why Orbit With Ben Views Are Still Low

**Date:** 2026-08-11 · **Status:** operating diagnosis (prioritisation, not hard causal claims)

## Executive summary

The channel is **distribution-starved, not technically broken**. It is about two weeks old, had one subscriber in the analytics snapshot, and has too little viewer history for YouTube to predict a dependable audience.

1. Shorts lose too many viewers in the opening seconds (**26.1%** stayed-to-watch vs **35%** working target).
2. Long-form has almost no discovery or conversion (**7** current views across two Public films; **25** audited long impressions; almost no browse/home).
3. Titles and technical settings are **not** the main blocker (title scores **86–98**; embeds, descriptions, language, canonical links, scheduling integrity repaired).

## Evidence window

Combines the current ~30-video catalogue snapshot with YouTube Analytics / vidIQ for **27 Jul–10 Aug 2026**. “Stayed to watch” = Shorts-feed viewers who stopped instead of swiping. Sample is tiny → supports prioritisation, not confident claims about thumbs/topics/times.

| Signal | Value |
|--------|------:|
| Shorts views (window) | 355 |
| Long views (window) | 6 |
| Shorts-feed share of attributed views | ~250 / 361 (~69%) |
| Search | ~13 (~4%) |
| Browse/home | effectively absent |
| Leading Short | 97 views |
| Top 3 Shorts share of current public views | ~181 / 232 (~78%) |

## Ranked constraints

| Rank | Constraint | Evidence | Confidence | Action |
|-----:|------------|----------|------------|--------|
| 1 | Weak Shorts opening retention | 26.1% stayed vs 35% target; ~19s AVD on 41–49s Shorts | High | Punch-first **22–30s** edits |
| 2 | Very little distribution history | ~14-day channel; 1 sub; no browse base | High | Stable release cadence |
| 3 | Shorts do not yet feed long-form | 355 Short vs 6 long views | High | Native Related + matching continuation |
| 4 | Long openings/packaging unproven | 25 long impressions; 7 current views | Medium | Strengthen first 30s; wait for CTR sample |
| 5 | Catalogue momentum interrupted | Cleanup/freeze delayed feed inventory | Medium | Let approved scheduled clusters run |
| 6 | SEO/titles | Scores 86–98; search only 13 views | Low as primary | Avoid mass retitling |

## Recommended next steps

1. Let scheduled topic clusters publish **without churn**. Do not flood with the three overlapping Private reserves.
2. Make next Shorts **22–30s** and punch-first (payoff/visual/question in frame one; payoff by ~20s).
3. Finish native Short→film funnel after each parent is Public (exact Related in Studio + verify).
4. Rebuild opening **30s** of future longs around one promise (no long logo/atmosphere preamble).
5. Judge creative after **5–10** new Shorts — before mass retitle/reschedule.

## Questions for the next release cycle

- Can punch-first 22–30s edits lift stayed-to-watch above 26.1%?
- Which topic family produces the strongest subs per 1,000 Short views?
- Once Related is active, what share of Short viewers open the parent film?
- Do long-form impressions grow enough for thumbnail CTR to become useful?

## Caveats

Tiny denominators. Live catalogue snapshot can lag/lead the vidIQ pull. 35% stayed-to-watch is an **internal** working target. Thumbnail CTR, first-30s curves, feed impressions, and Related CTR are not yet volume-ranked.

## Linked execution

- Sprint: `audits/punch_first_shorts_sprint_2026-08-11/PUNCH_FIRST_SHORTS_SPRINT.md`
- Punch batch (local): `PUNCH_FIRST_BATCH_INDEX.json`
- Related gates: `RELATED_VIDEO_RELEASE_GATES.md`
- Locked retention rules: `RETENTION_AND_GROWTH_LOCKED.md`
