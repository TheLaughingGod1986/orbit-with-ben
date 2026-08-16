# Next episode brief — Growth System v2

**Locked next (16 Aug 2026): 007 Neutron Star.** Script passed. Omni 1-min path (PR 18). Do not start 013 Moon. Simulation is 015.

Generated: 2026-08-06T14:05:59.670Z (snapshot below is historical; queue lock above is current)

**Candidate next topic:** 007 Neutron Star

## Channel snapshot (imported metrics)

| Metric | Value |
|---|---|
| Videos in sample | 2 |
| Impressions | 20000 |
| Views | 1320 |
| Avg CTR | 7.35% |
| Avg APV | 50.0% |
| Avg AVD (s) | 180 |
| Subs gained | 3 |
| Returning / new | 40 / 380 |

## Priorities for the next build

Apply these before writing the next cold open / packaging:

1. **[weak_opening]** What Really Happens When You Fall Into a Black Hole?: weak opening — 30s retention 48.0% (target ≥60%).
   - Action: Rewrite cold open: curiosity by 5s, stakes by 15s, journey by 30s. Cut definition/history opens. Put Orbit in danger/experience immediately.
2. **[weak_opening]** The Great Filter Fear: weak opening — 30s retention 55.0% (target ≥60%).
   - Action: Rewrite cold open: curiosity by 5s, stakes by 15s, journey by 30s. Cut definition/history opens. Put Orbit in danger/experience immediately.
3. **[runtime]** What Really Happens When You Fall Into a Black Hole?: long runtime (20 min) with APV 28.0%.
   - Action: Next videos: target 8–12 min until returning viewers and APV rise.
4. **[retention_drop]** What Really Happens When You Fall Into a Black Hole?: retention drop ~12 pts near 90s.
   - Action: Insert curiosity reset (new question / Orbit beat / number) before that timestamp. Avoid explain-dumps without story motion.
5. **[poor_title]** What Really Happens When You Fall Into a Black Hole?: CTR 3.50% on 12000 impressions (target ≥4%).
   - Action: Title underperforming — one promise, prefer ≤60 chars, no series suffix. Re-test title ABC with vidIQ ≥90.
6. **[needs_update]** What Really Happens When You Fall Into a Black Hole?: APV 28.0% below 35% floor.
   - Action: Consider trim to 8–12 min trust window, strengthen mid-film escalation, ensure Orbit agency every act.
7. **[traffic_mix]** What Really Happens When You Fall Into a Black Hole?: Search-heavy traffic (Search 70% · Browse+Suggested 15%).
   - Action: Improve session bridges (end screen/cards/pin to sibling docs) and Shorts Related funnel; strengthen hook retention so Browse/Suggested can trust the video.
8. **[funnel]** What Really Happens When You Fall Into a Black Hole?: end-screen CTR weak or missing.
   - Action: Configure end screen + cards to another Orbit documentary. Never leave a dead end.


## What is working (keep)

- Top hooks: mystery (APV 50.0%)
- Top topics: _(need more data)_
- Top Shorts: The Great Filter Fear (72.0% APV)

## Next episode locked defaults

- Runtime **8–12 min** · cold open 5s / 15s / 30s
- Orbit **experiences** the science · 4–6 acts
- CG: **Gemini Veo** · VO: **ElevenLabs** Ben Orbit Narrator
- 3–5 Shorts · curiosity-gap ends · Related → long
- Thumbs ABC + social mirror schedule after YouTube lock

## Gate before VO / Veo

```bash
cd 07_Content-Ops
npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>
```
