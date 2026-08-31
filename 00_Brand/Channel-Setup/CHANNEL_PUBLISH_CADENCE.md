# Orbit with Ben — publish cadence

Timezone: **Europe/London**  
Canonical strategy: `PUBLISHING_AND_SHORTS_STRATEGY.md`  
Source of truth: `OPTIMAL_PUBLISH_SCHEDULE.json`  
House + UAT/QA scoring bible: `ORBIT_HOUSE_AND_UAT_BIBLE.md` (locked 31 Aug 2026)  
Latest audit: `audits/CHANNEL_AUDIT_2026-08-25.md`  
Updated: **2026-08-31**

## Cadence rule

| Cadence | Slot | Time UK | Why |
|---------|------|---------|-----|
| **1 long-form / week** | **Thursday** | **18:00** Premiere | Pillar first · UK evening (locked house bible 31 Aug) |
| **5–7 Shorts / week** | **Thu evening → Wed** | **20:00** launch Short · **11:30** supporting | Support the pillar · midday discovery |

**Cluster:** Long first → Short #1 after 1–3h → one Short per day for Days 2–7.  
That week’s Shorts are punches from **that Thursday film only**. Studio Related → that long only. Zero `/go/` on Shorts. No new Short pins.

Never publish a teaser Short before the long is public.  
Never dump the full Shorts cluster on Day 1.  
Never use fearbait titles (even if vidIQ scores them higher).

---

## Cold-start override (until ≥500 views or ≥20 subs)

From audit **2026-08-25**: public Shorts still ~**30×** longs (~939 vs ~31 lifetime views). Punch length is fixed; wonder Shorts win; live longs stay cold.  
→ Keep daily Short support. Judge topics by Short velocity + stayed% (Studio refresh needed). Keepers target **+2 net/week**; review Europa week **10 Sep**. Do not remint Last Star leftovers. **Air window:** Last Star `REXYxuLOBoI` through Wed 2 Sep · Europa `NbW5G1BpPY0` Premiere Thu 3 Sep 18:00 · Neutron `Yk1tLh23rko` Premiere Thu 10 Sep 18:00. Next to **make:** **007 Neutron Star at 7–9 min** (not Moon / Simulation).

Historical note (2026-08-01 PM): Shorts ~100 / peak VPH ~53 vs long 5; BH then scheduled as `n7CbJrOCnU0` — live recut id is now `3xrxdmaOwJI`.

Re-run Studio / `vidiq_subscriber_insights` before moving clocks.

---

## Weekly pattern

```
Thu 18:00  →  Long-form Premiere (pillar · 7–9 min)
Thu 20:00  →  Short #1 (strongest hook)
Fri 11:30  →  Short #2
Sat 11:30  →  Short #3
Sun 11:30  →  Short #4
Mon 11:30  →  Short #5
Tue 11:30  →  Short #6
Wed 11:30  →  Short #7 (optional) + schedule next pillar
```

Default ops volume: **6 Shorts / long** (acceptable range **5–7**). Slot times match `.cursor/rules/orbit-publishing-shorts.mdc`.

---

## Launch window (live · audited 2026-08-01 PM)

| When | Asset | Status |
|------|-------|--------|
| **Live** | **V001 — Why Haven't We Found Aliens Yet?** | Public · `Mo93x0fxB1Q` · **5** views |
| **Live** | **Short #1 — Where Is Everybody? The Fermi Paradox** | Public · `z-DLqoSoEBo` · **100** views · wonder title locked (score 94) |
| **Sat 1 Aug 2026 · 12:30** | Short #2 — Space Is Rude About Distance | Scheduled · `UWwNKYf_aU8` |
| **Sun 2 Aug · 12:30** | Short #3 — What If Aliens Are Watching Us? | Scheduled · `MO19iXYCu0c` |
| **Mon 3 Aug · 12:30** | Short #4 — What If the First Alien Clue Is Already Here? | Scheduled · `--CxhjNqtSY` |
| **Tue 4 / Wed 5 Aug · 12:30** | Fermi Shorts #5–6 | **MISSING in Studio — fill gap** |
| **Thu 6 Aug · 19:00** | **V002 — Black Hole long** | Scheduled · `n7CbJrOCnU0` |
| **6 Aug 21:00 → 11 Aug 12:30** | V002 Shorts ×6 | Scheduled (`eZGAhF8dN7w` … `5nMieBeymKU`) |
| **Thu 21 Aug · 19:00** | **V003 — Alien Worlds long** | Scheduled · `b8-X_FyJnHM` |
| **21–26 Aug · 12:30** | V003 Shorts ×6 | Scheduled (`aX_7Qg_qzyo` … `i18OD5Ab748`) |

Confirm every schedule on Studio `/video/{id}/edit`. Every Short: desktop Studio **Related video pill** → that week’s Thursday long (required). **No new Short pins**; pin not required when Related is set. Zero `/go/`. Map: `.cursor/rules/orbit-shorts-related-video.mdc`.

---

## Content flywheel (every long)

5–7 Shorts · 3 X · 3 Threads · 2 LinkedIn · 3 Facebook · 1 Reddit · 1 Community poll · 1 Community image · (future: email + blog)

**Shorts auto-mirrors (when live on YouTube):**
- TikTok → `TikTok/AUTO_POST.md` (@orbitwithben)
- Instagram Reels + Facebook Page Reels → `Meta/AUTO_POST.md`

Template: `CONTENT_FLYWHEEL_TEMPLATE.md` · Checklist: `RELEASE_WEEK_CHECKLIST.md`

---

## Capacity

| Now (ops) | Later (aspirational) |
|-----------|----------------------|
| 4 longs / month · 20–28 Shorts / month | 2 longs / week when library + retention proven (≈ months 6–9+) |
