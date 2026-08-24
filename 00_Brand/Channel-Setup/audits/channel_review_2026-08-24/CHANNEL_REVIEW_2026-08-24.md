# Orbit with Ben — full channel review (24 Aug 2026)

**Goal set by Ben:** every new video reaches **1,000 views** by end of month.
**Data:** YouTube Data API pull 24 Aug 22:40 UK (`CHANNEL_STATS.json`) + Analytics API pull 23:15 (`CHANNEL_ANALYTICS.json` — enabled by Ben tonight).

## Analytics headlines (first real pull, last 30 days)

1. **Search is already 19% of views** (242/1,270) — the SEO pass is landing. Terms reaching us: "alien worlds", "exoplanets", "jwst", "zoo hypothesis", "3 suns". Keep search-first packaging.
2. **Shorts feed = 66%** of views; subscribers, notifications, browse ≈ nil — confirms the channel lives or dies by Shorts velocity right now.
3. **Loopability is the hidden lever.** Three Suns in the Sky: **717% average view percentage** — viewers watch it ~7x over. Next best: We Found Planets Made of Diamond 142%, JWST Textbook 123%. Build Shorts whose last frame flows into the first (seamless loop) — this multiplies watch time without more uploads.
4. **The funnel converts rarely but deeply:** Shorts→long link produced 1 click… that viewer watched **42 minutes**. Related-video produced 1 view = 18 minutes. Every funnel surface (pins, links, cards, end screens) is worth keeping even at low CTR.
5. **Long retention is the weak point:** Fermi film averages 2:22 of 18:31 (12.8%). Supports keeping new longs nearer 10–12 min until an audience exists.
6. Devices: 63% mobile. Geo: GB 498 (dominant), FR 17. 4 subs gained in 30 days — 3 came from Shorts.

---

## Where the channel is today

- **4 subscribers · 930 lifetime public views · 26 public videos** (25 live Shorts + longs; 27 more scheduled through 15 Sept).
- **Shorts = 97% of all views (901). Longs = 3% (29).**
- Every long so far: Fermi 10 · Black Hole 4 · Alien Worlds 10 · Last Star (premiere pending) 3 · JWST 2.

## What is working (keep doing)

1. **Daily Shorts cadence is compounding.** Views/day on new Shorts has climbed ~10x in 12 days:
   - 12 Aug batch: 0.2–4.7 views/day
   - 15 Aug: 17.6 · 20 Aug: 30.2 · 22 Aug: 41.5 · 24 Aug: **57/day (day one)**
   The algorithm is warming to the channel. Do not break the one-per-day rhythm.
2. **Concrete strange-image hooks win.** Top Shorts all state a specific, visual, slightly wrong-sounding fact:
   - Three Suns in the Sky — 141
   - Most of the Universe Gives Off No Light — 121
   - These Galaxies Appeared Too Early — 89
   - Why JWST Pictures Don't Match the Textbook — 83
   - Why This Alien World Looks Like a Giant Eye — 68
3. **Cluster ranking:** Alien Worlds 346 > JWST 288 (best views/day right now) > Last Star 124 > Fermi 100 > Black Hole 72. Exoplanets/JWST "strange discovery" material is the channel's pull; abstract physics explainers are weakest.
4. Packaging hygiene is now solid: every video has ~370–460ch vidIQ-derived tags, keyword-first descriptions, parent-film links + pinned comments on all live Shorts (done 22–24 Aug).

## What is failing (change)

1. **Long-form is invisible.** 29 views across five films. The Shorts→long funnel is not converting (JWST Shorts: 286 views → JWST long: 2). With 4 subscribers there is no Browse/Suggested seed audience, and 15–20 min films have nothing to bootstrap from.
2. **Generic/abstract titles die** even inside strong clusters: "Could Any of These Alien Worlds Host Life?" 26 · "The Hottest Nights in the Universe" 16 · "How Did Black Holes Get So Big So Fast?" 19.
3. **Day-one dumps kill velocity.** The 12 Aug batch (6 Shorts in one day) produced the five worst performers on the channel. The schedule rule (one/day at 12:30, Day-1 Short at 21:00) is correct — the violation was the failure.
4. **Packaging bugs shipped:** the five scheduled Last Star punch Shorts all had the identical long-form title + series suffix (fixed tonight — each now has a unique punch title + aligned description).
5. **No measurement loop.** Analytics API disabled → no CTR / retention / traffic-source data outside Studio. Flying blind on *why* videos win.

## Honest goal math

1,000 views/video in 7 days is a ~18x jump on the best Short and ~100x on longs — not reachable by tuning alone. What *is* realistic: keep Shorts velocity compounding (57/day day-one today → best recent Shorts should cross **150–400 within 2 weeks**, first 1k Short plausible inside September), and use Premiere week to give longs their first real audience. Treat 1k/video as the **system target for September**, with this week as the inflection.

## The plan to 1,000 views/video

### A. This week (Last Star premiere week — biggest single lever)

- Premiere Thu 27 Aug 18:00 UK (`REXYxuLOBoI`) with 5 unique-titled punch Shorts airing 26–29 Aug around it. All descriptions funnel to the premiere URL.
- Ben in Studio (agent cannot do these): confirm **end screens + cards** on the premiere and all live longs; **A/B/C thumbnail test** on the premiere; sit in Premiere chat at air time.
- Day-of: pin a comment on the premiere asking one question viewers can answer (comments in hour one are the strongest small-channel signal).

### B. Shorts engine (every week)

- **One Short per day, 12:30 UK, no dumps. Never ≥40s.**
- Every hook must pass the winner pattern: *a concrete strange image stated as fact* ("Three suns", "gives off no light", "appeared too early", "doesn't match the textbook"). Kill abstract question hooks unless the question contains the strange image.
- Lead Shorts scheduling with **JWST + Alien Worlds material** (highest velocity clusters). Fermi/Black Hole Shorts only with an exceptional hook.
- Keep Related-video + pinned full-film comment automation running on every Short as it goes public.

### C. Long-form (stop the bleed, then compound)

- **Do not raise production cost per long until a long clears ~200 views.** The Omni 1-minute pipeline for 007 Neutron Star is right; keep runtime nearer 10–12 min (retention doc P0-9 already says 8–12 min until trust is earned — the 18–25 min lock is premature for a 4-sub channel).
- Longs are currently **search assets, not Browse assets**: title/desc/tags target one search phrase exactly (done in the SEO pass). Expect slow accumulation, not day-one spikes.
- The channel trailer is now set (JWST film) so channel-page visitors from Shorts see a full film immediately.

### D. Measurement (unblocks everything else)

- **Ben action (2 min):** enable YouTube Analytics API → https://console.developers.google.com/apis/api/youtubeanalytics.googleapis.com/overview?project=1053796460911 — then `npx tsx scripts/_channel_analytics_2026-08-24.ts` gives weekly CTR / retention / traffic-source scorecards. Until then, read Studio → Analytics → Content per video weekly: swipe-away rate on Shorts, impressions CTR on longs.
- Weekly scorecard habit (P1-19 in the locked growth doc): log to `RETENTION_LEARNINGS.md`.

### E. September cadence (compounding month)

- Thu 3 Sept: Europa premiere + 9 scheduled Europa Shorts (3–10 Sept) — already packaged, unique titles, funnels in place.
- Thu 10 Sept: Neutron Star long + 6 punch Shorts (10–15 Sept) — already scheduled.
- Build 007 minute-by-minute per the locked pipeline; pre-build vidIQ audit before any new script.
- **Consistency is the strategy:** by mid-Sept the channel will have ~45 live Shorts feeding 7 longs across 7 topic clusters, all cross-linked.

## Applied tonight (channel optimizations)

| Change | Detail |
|---|---|
| 5 Last Star Shorts retitled | unique punch-first titles + realigned descriptions (were all identical) |
| Channel trailer set | `ziKBPJ6FY0U` (JWST film) for unsubscribed visitors |
| SEO pass (earlier today) | all 53 uploads: tags 370–460ch, keyword-first descs, parent links |
| Schedule doc fixed | stale "Shorts 30–60s" line → locked 20–28s punch-first |
| Analytics API live | first pull saved to `CHANNEL_ANALYTICS.json`; headlines above |
| **End screens: all 7 longs** | 1 video (Best for viewer) + Subscribe, last ~20s — Fermi/AW/Europa added tonight via browser automation; BH/JWST/Last Star/Neutron already had them. Verified per video. |
| **Info cards: all 7 longs** | one mid-film video card each, cross-cluster (Fermi→AW 7:30 · BH→JWST 8:30 · AW→Fermi 8:30 · JWST→**Last Star premiere** 6:30 · Last Star→JWST 3:30 · Europa→AW 3:45 · Neutron→BH 4:00). Times verified by reload. |
| Last Star thumbs B + C built | `last-star_thumb_B_final-sunset` (emotion) + `last-star_thumb_C_what-comes-after` (question) in `005_…/08_Thumbnail/Selected/` — completes the object/emotion/question ABC set |

Artifacts: `studio_finish/STUDIO_FINISH_RESULT.json` + screenshots.

## Open items for Ben

1. **"Verify that it's you"** — Studio blocked the thumbnail A/B test start with a Google verification wall (screenshot `studio_finish/v2_ab_list.png`). A Studio tab is open in your Chrome: complete the Verify prompt, then say "verified" and the A/B/C test on the Last Star premiere gets re-run (B+C are staged and ready).
2. `SdNXS1PD_Yk` — leaving public as you decided; it funnels premiere-day traffic.
3. vidIQ A/B history note: Fermi + Black Hole thumbnail tests finished "no clear winner" (too few impressions); Alien Worlds test in progress ends ~27 Aug. Don't read anything into those results yet — the channel needs more impressions for tests to resolve.
